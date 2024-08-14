from django.contrib import admin
from django.urls import path
from management import views
from django.views.generic import TemplateView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("",views.index,name='home'),
    path("about",views.about,name='about'),
    path("contact",views.contact,name='contact'),
    path("professor",views.professor,name='professor'),
    path("student",views.student,name='student'),
    path("login_professor",views.login_professor,name='login_professor'),
    path("login_student",views.login_student,name='login_student'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_success/', TemplateView.as_view(template_name="password_reset_success.html"), name='password_reset_success'),
    path("professor_dashboard",views.professor_dashboard,name='professor_dashboard'),
    path('marks1',views.marks1,name='marks1'),
    path('marks2',views.marks2,name='marks2'),
    path('attendance1',views.attendance1,name='attendance1'),
    path('attendance2',views.attendance2,name='attendance2'),
    path('notice1',views.notice1,name='notice1'),
    path('notice_all',views.notice_all,name='notice_all'),
    path('notice_selected',views.notice_selected,name='notice_selected'),
    path("student_dashboard",views.student_dashboard,name='student_dashboard'),
    path('student_marks',views.student_marks,name='student_marks'),
    path('student_attendance',views.student_attendance,name='student_attendance'),
    path('subject_details',views.subject_details,name='subject_details'),
    path('payment1',views.payment1,name='payment1'),
    path('forgot_password_s/', views.forgot_password_s, name='forgot_password_s'),
    path('verify_otp_s/', views.verify_otp_s, name='verify_otp_s'),
    path('reset_password_s/', views.reset_password_s, name='reset_password_s'),
]
