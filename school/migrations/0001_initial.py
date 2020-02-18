# Generated by Django 2.2 on 2020-02-14 08:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_lecturer', models.BooleanField(default=False)),
                ('is_librarian', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=60, null=True)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to="users/pictures/%Y/%m/%d'")),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('password_type', models.CharField(choices=[('Expirable', 'Expirable'), ('None-Expirable', 'None-Expirable')], default='Expirable', max_length=200, verbose_name='Password Type')),
                ('last_password_reset_date', models.DateField(auto_now=True, verbose_name='Reset On')),
                ('password_expiry_date', models.DateField(blank=True, editable=False, null=True)),
                ('is_password_expired', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllDepartmentsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentname', models.CharField(default='', max_length=200, verbose_name='Name Of Department')),
            ],
            options={
                'verbose_name': 'All School Departments',
                'verbose_name_plural': 'All School Departments',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseTitle', models.CharField(max_length=200)),
                ('courseCode', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('is_elective', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Fee To Be Paid')),
            ],
            options={
                'verbose_name': 'Fee Structure',
                'verbose_name_plural': 'Fees Structure',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=200, verbose_name='Grade')),
            ],
            options={
                'verbose_name': 'Level/Grade',
                'verbose_name_plural': 'Levels/Grades',
            },
        ),
        migrations.CreateModel(
            name='PasswordConfigurations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(default='All Users', help_text='e.g Student', max_length=200, verbose_name='User Type')),
                ('number_of_days_to_expire', models.IntegerField(default=30, verbose_name='Days')),
            ],
            options={
                'verbose_name': 'Password Configuration',
                'verbose_name_plural': 'Password Configurations',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(default='', help_text='name of class, (eg. A)', max_length=200, verbose_name='Enter Class Title')),
                ('classteacher', models.ForeignKey(default='', max_length=200, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Assign Teacher')),
                ('courses', models.ManyToManyField(help_text='Hold Ctrl to choose multiple', related_name='class_subject', to='school.Course', verbose_name='Choose Courses')),
                ('grade', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Level', verbose_name='Level')),
            ],
            options={
                'verbose_name': 'School Class',
                'verbose_name_plural': 'School Classes',
            },
        ),
        migrations.CreateModel(
            name='SchoolDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolname', models.CharField(default='', max_length=500, verbose_name='Name Of School')),
                ('address', models.CharField(blank=True, default='School Address', max_length=200, null=True, verbose_name='School Address')),
                ('email', models.CharField(blank=True, default='exampleemail@exampleemail.com', max_length=200, null=True, verbose_name='Email Address')),
                ('facebook', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Facebook Page Link')),
                ('twitter', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Twitter')),
                ('instagram', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Instagram')),
                ('phone', models.CharField(blank=True, default='Tel/Cell Number', max_length=200, null=True, verbose_name='Tel/Cell')),
                ('photo', models.ImageField(blank=True, default='', null=True, upload_to='school/logo/%Y/%m/%d', verbose_name='School logo')),
            ],
            options={
                'verbose_name': 'School Details',
                'verbose_name_plural': 'School Details',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(blank=True, choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third')], max_length=10)),
                ('is_current_semester', models.BooleanField(blank=True, default=False, null=True)),
                ('next_semester_begins', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=200, unique=True)),
                ('is_current_session', models.BooleanField(blank=True, default=False, null=True)),
                ('next_session_begins', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=20, unique=True)),
                ('enrollment_date', models.DateField(auto_now_add=True, null=True)),
                ('level', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Level', verbose_name='Grade')),
                ('schoolclass', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.SchoolClass', verbose_name='Class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_exam_marking', models.BooleanField(default=False)),
                ('exam_start_marking_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thur', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], max_length=20, verbose_name='Day')),
                ('start_time', models.TimeField(verbose_name='Start Time')),
                ('end_time', models.TimeField(verbose_name='End Time')),
                ('venue', models.CharField(blank=True, help_text='Optional', max_length=200, null=True, verbose_name='Venue')),
                ('description', models.CharField(blank=True, help_text='Optional', max_length=200, null=True, verbose_name='Description')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TakenCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ca', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('exam', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('grade', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], max_length=1)),
                ('comment', models.CharField(blank=True, choices=[('PASS', 'PASS'), ('FAIL', 'FAIL')], max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taken_courses', to='school.Course')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
            ],
        ),
        migrations.AddField(
            model_name='semester',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Session'),
        ),
        migrations.CreateModel(
            name='SchoolFees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amountpaid', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Total Amount Paid')),
                ('actualamountpaid', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Actual Amount Paid')),
                ('balance', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Balance')),
                ('paystatus', models.CharField(blank=True, default='Fully Paid', editable=False, max_length=30, null=True)),
                ('paymentdate', models.DateField(auto_now=True, verbose_name='Paid On')),
                ('total', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Fees To Be Paid')),
                ('gradefees', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Fees', verbose_name='Choose Fees Structure')),
                ('semester', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Semester', verbose_name='Choose Academic Term')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Student', verbose_name='Choose Student')),
            ],
            options={
                'verbose_name': 'School Fees',
                'verbose_name_plural': 'School Fees',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpa', models.FloatField(null=True)),
                ('cgpa', models.FloatField(null=True)),
                ('semester', models.CharField(choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third')], max_length=100)),
                ('session', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Course')),
                ('level', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Level', verbose_name='Level')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
            ],
        ),
        migrations.CreateModel(
            name='PupilAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_attendance', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Present', max_length=50)),
                ('daysdate', models.DateField(default='', verbose_name='Attended On')),
                ('nameofclass', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.SchoolClass', verbose_name='Class')),
                ('student', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student Attendance',
                'verbose_name_plural': 'Student Attendance',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(blank=True, max_length=200, null=True, verbose_name='Occupation')),
                ('nationality', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nationality')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fees',
            name='grade',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Level', verbose_name='Level'),
        ),
        migrations.CreateModel(
            name='ExamTimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('venue', models.CharField(blank=True, max_length=200, null=True)),
                ('additional_info', models.TextField(blank=True, max_length=1000, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Semester')),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentOfTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(default='', max_length=200, verbose_name='Teacher')),
                ('department', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.AllDepartmentsList', verbose_name='Name Of Department')),
            ],
            options={
                'verbose_name': 'Teacher And Department',
                'verbose_name_plural': 'Teacher And Department',
            },
        ),
        migrations.CreateModel(
            name='CourseAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ManyToManyField(related_name='allocated_course', to='school.Course')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Session')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='school.Level', verbose_name='Grade'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Semester'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.TextField(max_length=10000, verbose_name='News Details')),
                ('announcementdatetime', models.DateTimeField(auto_now=True, verbose_name='Date')),
                ('teacher', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Teachers Name')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='days_for_password_expiry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.PasswordConfigurations'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
