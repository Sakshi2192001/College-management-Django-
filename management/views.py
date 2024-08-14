from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Professor_info,Student_info,professor_class_mapp,StudentMarks,StudentAttendance,professor_sub_mapp,contactus
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMessage
from .forms import EmailForm, OTPForm, PasswordResetForm,StudentMarksForm,StudentAttendanceForm
from .utils import generate_otp
from django.db import connection
from django.db.models import F
import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        c=contactus(name=name,email=email,subject=subject,message=message)
        c.save()             #save c so data save in database
        messages.success(request,"Message has been sent.")
    return render(request,'contact.html')
def professor(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        address=request.POST.get('address')
        aadhar_number=request.POST.get('aadhar_number')
        professor_id=request.POST.get('professor_id')
        password=request.POST.get('password')
        professor=Professor_info(name=name,email=email,phone_number=phone_number,address=address,aadhar_number=aadhar_number,professor_id=professor_id,password=password)
        professor.save()
       
        messages.success(request,'Professor details updated!!')
    return render(request,'professor.html')
def student(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        address=request.POST.get('address')
        aadhar_number=request.POST.get('aadhar_number')
        year=request.POST.get('year')
        student_id=request.POST.get('student_id')
        password=request.POST.get('password')
        student=Student_info(name=name,email=email,phone_number=phone_number,address=address,aadhar_number=aadhar_number,year=year,student_id=student_id,password=password)
        student.save()
       
        messages.success(request,'Student details updated!!')
    return render(request,'student.html')

def login_professor(request):

    if request.method=="POST":
        username=request.POST.get('email-phone')
        password=request.POST.get('id')
        if username and password:
            # Check if the identifier is an email
            try:
                validate_email(username)
                professor = Professor_info.objects.get(email=username, password=password)
                request.session['p_name']=professor.name
                request.session['p_id']=professor.professor_id
                return redirect('professor_dashboard')  # Redirect to the dashboard if the teacher exists
            except ValidationError:
                # If not an email, treat it as a phone number
                try:
                    professor = Professor_info.objects.get(phone_number=username, password=password)
                    request.session['p_name']=professor.name
                    request.session['p_id']=professor.professor_id
                    return redirect('professor_dashboard')  # Redirect to the dashboard if the teacher exists
                except Professor_info.DoesNotExist:
                    messages.error(request, 'Invalid email/phone number or password')
            except Professor_info.DoesNotExist:
                messages. error(request, 'Invalid email/phone number or password')
        else:
            messages. error(request, 'Email/Phone number and password are required')
        return render(request, 'login_professor.html')
    return render(request, 'login_professor.html')

def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(f"Email entered: {email}")  # Debugging print statement  ,f->string
            try:
                # Ensure case-insensitive comparison of email
                professor = Professor_info.objects.get(email__iexact=email)
                print(f"Professor found: {professor.email}")  # Debugging print statement
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'sakshi2192001@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_otp')
            except Professor_info.DoesNotExist:
                print(f"Professor with email {email} does not exist")  # Debugging print statement
                form.add_error('email', 'Email does not exist')
        else:
            print("Form is not valid")  # Debugging print statement
    else:
        form = EmailForm()
    return render(request, 'forgot_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                return redirect('reset_password')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = request.session.get('email')
            if email:
                try:
                    Professor_info.objects.filter(email=email).update(password=new_password)
                    request.session.flush()
                    return redirect('password_reset_success')
                except Professor_info.DoesNotExist:
                    form.add_error(None, 'User does not exist')
    else:
        form = PasswordResetForm()   #class made like this if request.method is not post
    return render(request, 'reset_password.html', {'form': form})

def professor_dashboard(request):
    name = request.session.get('p_name')
    id = request.session.get('p_id')
    years = professor_class_mapp.objects.filter(professor_id=id).values_list('year_of_stud', flat=True).distinct()
    return render(request, 'professor_dashboard.html', {'professor_name': name, 'years': years})

def marks1(request):
    name = request.session.get('p_name')
    id = request.session.get('p_id')
    years = professor_class_mapp.objects.filter(professor_id=id).values_list('year_of_stud', flat=True).distinct()
    if request.method=="POST":
        year_id=request.POST.get('year')
        request.session['y']=year_id     #to save year in y
        return redirect('marks2')
    return render(request, 'marks1.html', {'professor_name': name, 'years': years})

def marks2(request):
    year_id=request.session.get('y')
    students = Student_info.objects.filter(year=year_id)
    forms=[]
    for student in students:
        student_marks, created = StudentMarks.objects.get_or_create(student=student)
        forms.append((student, StudentMarksForm(instance=student_marks, prefix=str(student.student_id))))
    if request.method == 'POST':
          for student, form in forms:
            form = StudentMarksForm(request.POST, prefix=str(student.student_id), instance=StudentMarks.objects.get(student=student))
            if form.is_valid():
                    student_marks.dsa = form.cleaned_data.get('dsa')
                    student_marks.os = form.cleaned_data.get('os')
                    student_marks.save()
                    send_mail(
                        'Regarding Marks',
                        f'hello {student_marks.student.name} your marks has been uploaded',
                        'sakshi2192001@gmail.com',
                        [student_marks.student.email],
                        fail_silently=False,
                    )
        # return redirect('marks2')
            return redirect('marks2')
    return render(request, 'marks2.html', {'forms': forms, 'year_id': year_id})

def attendance1(request):
    name = request.session.get('p_name')
    id = request.session.get('p_id')
    years = professor_class_mapp.objects.filter(professor_id=id).values_list('year_of_stud', flat=True).distinct()
    if request.method=="POST":
        year_id=request.POST.get('year')
        request.session['y']=year_id     #to save year in y
        return redirect('attendance2')
    return render(request, 'attendance1.html', {'professor_name': name, 'years': years})

def attendance2(request):
    year_id=request.session.get('y')
    students = Student_info.objects.filter(year=year_id)
    forms=[]
    for student in students:
        student_attendance, created = StudentAttendance.objects.get_or_create(student=student)
        forms.append((student, StudentAttendanceForm(instance=student_attendance, prefix=str(student.student_id))))
    if request.method == 'POST':
          for student, form in forms:
            form = StudentAttendanceForm(request.POST, prefix=str(student.student_id), instance=StudentAttendance.objects.get(student=student))
            if form.is_valid():
                    student_attendance.attendance_dsa = form.cleaned_data.get('attendance_dsa')
                    student_attendance.attendance_os = form.cleaned_data.get('attendance_os')
                    student_attendance.save()
                    send_mail(
                        'Regarding Attendance',
                        f'hello {student_attendance.student.name} your attendance has been updated',
                        'sakshi2192001@gmail.com',
                        [student_attendance.student.email],
                        fail_silently=False,
                    )
        # return redirect('marks2')
            return redirect('attendance2')
    return render(request, 'attendance2.html', {'forms': forms, 'year_id': year_id})

def notice1(request):
    name = request.session.get('p_name')
    id = request.session.get('p_id')
    years = professor_class_mapp.objects.filter(professor_id=id).values_list('year_of_stud', flat=True).distinct()
    if request.method=="POST":
        year_id=request.POST.get('year')
        request.session['y']=year_id     #to save year in y
        email_option = request.POST.get('email_option')
        if email_option == 'all':
            return redirect('notice_all')
        elif email_option == 'selected':
            return redirect('notice_selected')
    return render(request, 'notice1.html', {'professor_name': name, 'years': years})

def notice_all(request):
    year=request.session.get('y')
    if request.method == 'POST':
        message = request.POST.get('message')
        students = Student_info.objects.filter(year=year)
        recipient_list = [student.email for student in students]

        to_email = recipient_list[0]
        cc_emails = recipient_list[1:]

        # Create an EmailMessage object
        email = EmailMessage(
            'New Notice has been Published',
            message,
            'sakshi2192001@gmail.com',
            [to_email],
            cc=cc_emails,
        )

        # Send the email
        email.send(fail_silently=False)
        messages.success(request,"Notice has been sent to all.")
        #return redirect('success_url')  # Replace with your success URL

    return render(request, 'notice_all.html')

def notice_selected(request):
    year=request.session.get('y')
    if request.method == 'POST':
        message = request.POST.get('message')
        selected_emails = request.POST.getlist('emails')

        to_email = selected_emails[0]
        cc_emails = selected_emails[1:]

        # Create an EmailMessage object
        email = EmailMessage(
            'New Notice has been Published',
            message,
            'sakshi2192001@gmail.com',
            [to_email],
            cc=cc_emails,
        )

        # Send the email
        email.send(fail_silently=False)
        messages.success(request,"Notice has been sent.")
        #return redirect('success_url')  # Replace with your success URL

    students = Student_info.objects.filter(year=year)
    return render(request, 'notice_selected.html', {'students': students})



def login_student(request):

    if request.method=="POST":
        username=request.POST.get('email-phone')
        password=request.POST.get('id')
        if username and password:
            # Check if the identifier is an email
            try:
                validate_email(username)
                student = Student_info.objects.get(email=username, password=password)
                request.session['s_name']=student.name
                request.session['s_id']=student.student_id
                request.session['s_year']=student.year
                return redirect('student_dashboard')  # Redirect to the dashboard if the student exists
            except ValidationError:
                # If not an email, treat it as a phone number
                try:
                    student = Student_info.objects.get(phone_number=username, password=password)
                    request.session['s_name']=student.name
                    request.session['s_id']=student.student_id
                    request.session['s_year']=student.year
                    return redirect('student_dashboard')  # Redirect to the dashboard if the student exists
                except Student_info.DoesNotExist:
                    messages.error(request, 'Invalid email/phone number or password')
            except Student_info.DoesNotExist:
                messages. error(request, 'Invalid email/phone number or password')
        else:
            messages. error(request, 'Email/Phone number and password are required')
        return render(request, 'login_student.html')
    return render(request, 'login_student.html')

def student_dashboard(request):
    name = request.session.get('s_name')
    return render(request, 'student_dashboard.html', {'student_name': name})

def student_marks(request):
    name = request.session.get('s_name')
    id = request.session.get('s_id')
    student_marks = get_object_or_404(StudentMarks, student_id=id)

    if student_marks.dsa == "":
        m_dsa = "Marks has not been uploaded"
        dsa_status = ""
    else:
        m_dsa = student_marks.dsa
        if int(m_dsa) < 40:
            dsa_status = "Fail"
        else:
            dsa_status = "Pass"

    if student_marks.os == "":
        m_os = "Marks has not been uploaded"
        os_status = ""
    else:
        m_os = student_marks.os
        if int(m_os) < 40:
            os_status = "Fail"
        else:
            os_status = "Pass"

    return render(request, 'student_marks.html', {
        'name': name,
        'm_dsa': m_dsa,
        'dsa_status': dsa_status,
        'm_os': m_os,
        'os_status': os_status
    })

def student_attendance(request):
    name = request.session.get('s_name')
    id = request.session.get('s_id')
    student_attendance = get_object_or_404(StudentAttendance, student_id=id)

    if student_attendance.attendance_dsa == "":
        a_dsa = "Attendance has not been updated"
        dsa_status = ""
    else:
        a_dsa = student_attendance.attendance_dsa
        if int(a_dsa) < 70:
            dsa_status = "Low"
        else:
            dsa_status = "Good"

    if student_attendance.attendance_os == "":
        a_os = "Attendance has not been updated"
        os_status = ""
    else:
        a_os = student_attendance.attendance_os
        if int(a_os) < 70:
            os_status = "Low"
        else:
            os_status = "Good"

    return render(request, 'student_attendance.html', {
        'name': name,
        'a_dsa': a_dsa,
        'dsa_status': dsa_status,
        'a_os': a_os,
        'os_status': os_status
    })

def subject_details(request):
    year=request.session.get('s_year') 
    professor_class_mappings = professor_class_mapp.objects.filter(year_of_stud=year)
    
    
    # Prepare a list of teachers with their subjects
    Professor_info = []
    for mapping in professor_class_mappings:
        professor = mapping.professor
        subjects = professor_sub_mapp.objects.filter(
            professor=professor,
        ).values_list('subject', flat=True)
        print(f"Teacher: {professor.name}, Subjects: {list(subjects)}")
        Professor_info.append({
            'name': professor.name,
            'email': professor.email,
            'subjects': ', '.join(subjects)  # Join subjects into a comma-separated string
        })
    
    return render(request, 'subject_details.html', {'year': year, 'Professor_info': Professor_info})

def payment1(request):

    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount':50000*100,'currency':'INR','payment_capture':1})


    return render(request,'payment1.html',{'order_id':payment['id']})


def forgot_password_s(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(f"Email entered: {email}")  # Debugging print statement  ,f->string
            try:
                # Ensure case-insensitive comparison of email
                student = Student_info.objects.get(email__iexact=email)
                print(f"Student found: {student.email}")  # Debugging print statement
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'sakshi2192001@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_otp_s')
            except Student_info.DoesNotExist:
                print(f"Student with email {email} does not exist")  # Debugging print statement
                form.add_error('email', 'Email does not exist')
        else:
            print("Form is not valid")  # Debugging print statement
    else:
        form = EmailForm()
    return render(request, 'forgot_password_s.html', {'form': form})

def verify_otp_s(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                return redirect('reset_password_s')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp_s.html', {'form': form})

def reset_password_s(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = request.session.get('email')
            if email:
                try:
                    Student_info.objects.filter(email=email).update(password=new_password)
                    request.session.flush()
                    return redirect('password_reset_success')
                except Student_info.DoesNotExist:
                    form.add_error(None, 'User does not exist')
    else:
        form = PasswordResetForm()   #class made like this if request.method is not post
    return render(request, 'reset_password_s.html', {'form': form})
