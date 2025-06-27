from django.shortcuts import render, get_object_or_404, redirect
from .models import EmployeeDetails, ServerDetails, AccessDetails
from django.db.models import Count, Q, F, OuterRef, Subquery
from django.contrib import messages 
import pandas as pd
import re
from fuzzywuzzy import fuzz
import jellyfish
import io 


from .forms import UsernameCSVUploadForm, EmployeeForm, AccessDetailsForm


def homepage(request):
    query = request.GET.get('query', '').strip()
    servers = []

    subquery = AccessDetails.objects.filter(email=OuterRef('email')).values('email').annotate(
        server_count=Count('server_name', distinct=True)).values('server_count')

    employees = EmployeeDetails.objects.annotate(server_count=Subquery(subquery[:1])).filter(server_count__gt=0).order_by('emp_id')

    server_count_subquery = AccessDetails.objects.filter(server_name=OuterRef('server_name')).values(
        'server_name').annotate(server_count=Count('server_name')).values('server_count')

    server_details_with_count = ServerDetails.objects.annotate(server_count=Subquery(server_count_subquery[:1])).order_by('server_name')

    if query.lower().endswith(".com"):
        servers = server_details_with_count.filter(server_name__icontains=query)
    elif query:
        employees = employees.filter(
            Q(emp_id__icontains=query) | Q(name__icontains=query)
        )
        servers = server_details_with_count.filter(app__icontains=query)

   
    return render(request, 'homepage.html', {'employees': employees, 'servers': servers, 'query': query})


def employee_detail(request, emp_id):
    employee = get_object_or_404(EmployeeDetails, emp_id=emp_id)
   
    return render(request, 'employee_detail.html', {'employee': employee})


def edit_employee(request, emp_id):
    employee = get_object_or_404(EmployeeDetails, emp_id=emp_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {employee.name} updated successfully!")
            return redirect('employee_detail', emp_id=employee.emp_id)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


def server_list(request):
    server_data = (
        AccessDetails.objects
        .values('server_name')
        .annotate(employee_count=Count('user_name'))
        .order_by('server_name')
    )
   
    return render(request, 'server_list.html', {'server_data': server_data})


def apps_list(request):
    app_data = (
        AccessDetails.objects
        .values('app')
        .annotate(employee_count=Count('email'))
        .order_by('app')
    )
   
    return render(request, 'apps_list.html', {'app_data': app_data})


def data(request):
    type_param = request.GET.get('type', None)
    name = request.GET.get('name', None)
    filter_criteria = None

    emp_subquery = EmployeeDetails.objects.filter(email=OuterRef('email')).values('emp_id')
    access_details = AccessDetails.objects.annotate(emp_id=Subquery(emp_subquery[:1])).order_by('access_key')

    if type_param:
        filtered_data = access_details.filter(
            Q(server_name__icontains=name) |
            Q(app__icontains=name) |
            Q(emp_id__icontains=name)
        ).order_by('access_key')
        filter_criteria = {'type': type_param, 'value': name}
    else:
        filtered_data = access_details
   
    return render(request, 'access_details.html', {'access_details': filtered_data,'filter_criteria':filter_criteria})


def access_detail(request, access_key):
    access_detail = get_object_or_404(AccessDetails, access_key=access_key)
   
    return render(request, 'access_detail_page.html', {'access_detail': access_detail})


def edit_access_details(request, access_key):
    access_detail = get_object_or_404(AccessDetails, access_key=access_key)

    if request.method == 'POST':
        form = AccessDetailsForm(request.POST, instance=access_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f"Access detail for {access_detail.user_name} updated successfully!")
            return redirect('access_detail_page', access_key=access_key)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = AccessDetailsForm(instance=access_detail)
    
    return render(request, 'edit_access_details.html', {'form': form, 'access_detail': access_detail})




def compute_match_score(username, employee_name, first_name, last_name, emp_id):
    """
    Computes a match score between a username and employee details.
    Uses various string matching algorithms (Levenshtein, Soundex, Metaphone)
    and pattern matching.
    """
    username_lower = str(username).lower().strip()
    employee_name_lower = str(employee_name).lower().strip()
    first_name_lower = str(first_name).lower().strip()
    last_name_lower = str(last_name).lower().strip()
    emp_id_str = str(emp_id).lower().strip()

    username_parts = re.split(r'[\._\-\s]', username_lower)
    part1 = username_parts[0] if len(username_parts) > 0 else ''
    part2 = username_parts[1] if len(username_parts) > 1 else ''

    
    possible_patterns = [
        f"{first_name_lower}.{last_name_lower}",
        f"{last_name_lower}.{first_name_lower}",
        f"{first_name_lower}_{last_name_lower}",
        f"{last_name_lower}_{first_name_lower}",
        f"{first_name_lower}{last_name_lower}",
        f"{last_name_lower}{first_name_lower}",
        f"{first_name_lower} {last_name_lower}",
        f"{last_name_lower} {first_name_lower}"
    ]
    if username_lower in possible_patterns:
        return 100.0

   
    split_bonus = 0
    if ((part1 == first_name_lower and part2 == last_name_lower) or
        (part2 == first_name_lower and part1 == last_name_lower)):
        split_bonus += 10

    
    number_match_bonus = 0
    if emp_id_str and emp_id_str in username_lower:
        number_match_bonus += 5

    
    lev_full = fuzz.ratio(username_lower, employee_name_lower)
    partial_full = fuzz.partial_ratio(username_lower, employee_name_lower)
    token_set_full = fuzz.token_set_ratio(username_lower, employee_name_lower)

    token_set_first = fuzz.token_set_ratio(username_lower, first_name_lower)
    token_set_last = fuzz.token_set_ratio(username_lower, last_name_lower)

    
    soundex_match_last = int(jellyfish.soundex(username_lower) == jellyfish.soundex(last_name_lower))
    metaphone_match_last = int(jellyfish.metaphone(username_lower) == jellyfish.metaphone(last_name_lower))
    soundex_match_first = int(jellyfish.soundex(username_lower) == jellyfish.soundex(first_name_lower))
    metaphone_match_first = int(jellyfish.metaphone(username_lower) == jellyfish.soundex(first_name_lower))

    
    initial_bonus = 0
    if username_lower and first_name_lower and username_lower[0] == first_name_lower[0]:
        initial_bonus += 5
    if '.' in username_lower:
        parts = username_lower.split('.')
        if len(parts) > 1 and first_name_lower and parts[1] and parts[1][0] == first_name_lower[0]:
            initial_bonus += 5

   
    composite = (
        (lev_full * 0.2) +
        (partial_full * 0.2) +
        (token_set_full * 0.2) +
        (token_set_last * 0.3) +
        (token_set_first * 0.2) +
        (soundex_match_last * 6) +
        (metaphone_match_last * 7) +
        (soundex_match_first * 3) +
        (metaphone_match_first * 3) +
        split_bonus +
        initial_bonus +
        number_match_bonus
    )
    return min(composite, 100.0)


def unauthorized_employees(request):
    unmatched_usernames = None 
    form = UsernameCSVUploadForm() 

    if request.method == 'POST':
        form = UsernameCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                csv_file_buffer = io.BytesIO(csv_file.read())
                df_usernames = pd.read_csv(csv_file_buffer)
                
                if 'username' not in df_usernames.columns.str.lower():
                    username_col_name = df_usernames.columns[0]
                    df_usernames.rename(columns={username_col_name: 'username'}, inplace=True)
                else:
                    username_col_name = df_usernames.columns[df_usernames.columns.str.lower() == 'username'][0]
                    df_usernames.rename(columns={username_col_name: 'username'}, inplace=True)

            except Exception as e:
                messages.error(request, f"Error reading CSV file: {e}. Please ensure it's a valid CSV.")
               
                return render(request, 'unauthorized_employees_content.html', {'form': form, 'unmatched_usernames': None})

            employees_from_db = EmployeeDetails.objects.all()
            
            unmatched_usernames_list = [] 

            for _, username_row in df_usernames.iterrows():
                username = username_row['username']
                
                best_match_score = 0
                found_strong_match = False
                for employee_db in employees_from_db:
                    employee_name_parts = employee_db.name.split(' ', 1)
                    first_name = employee_name_parts[0] if employee_name_parts else ''
                    last_name = employee_name_parts[1] if len(employee_name_parts) > 1 else ''

                    score = compute_match_score(
                        username=username,
                        employee_name=employee_db.name,
                        first_name=first_name,
                        last_name=last_name,
                        emp_id=employee_db.emp_id
                    )

                    if score > best_match_score:
                        best_match_score = score
                    
                    if score >= 50:
                        found_strong_match = True
                        break 

                if not found_strong_match:
                    unmatched_usernames_list.append({'username': username})
            
            unmatched_usernames_list.sort(key=lambda x: x['username'])
            unmatched_usernames = unmatched_usernames_list 

        else: 
            messages.error(request, "Error uploading file. Please correct the errors below.")
                
        print(f"DEBUG: Attempting to render 'unauthorized_employees_content.html'")
        print(f"DEBUG: Form object type: {type(form)}")
        print(f"DEBUG: Unmatched usernames data type: {type(unmatched_usernames)}")
        return render(request, 'unauthorized_employees_content.html', {
        'unmatched_usernames': unmatched_usernames
    })
    if unmatched_usernames:
        print(f"DEBUG: First few unmatched usernames: {unmatched_usernames[:3]}")
    
    return render(request, 'unauthorized_employees_content.html', {
        'form': form
    })

