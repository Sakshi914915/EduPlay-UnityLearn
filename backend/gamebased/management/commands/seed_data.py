"""
Seed Data Management Command for EduPlay - UnityLearn
Populates Supabase PostgreSQL with rich, realistic data for all 6 modules.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Badge, UserBadge
from gamebased.models import Category, Quiz, Question, Option, QuizAttempt
from simulations.models import SimulationCategory, Simulation
from learningpaths.models import Subject, Course, CourseModule, Lesson, Enrollment
from collaborative.models import StudyGroup, Forum, ForumPost, PostComment
from analytics.models import ActivityLog, DailyProgress, UserAnalytics
from authoring.models import ContentTemplate, ContentDraft, CustomQuizBuilder
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = '🌱 Seeds Supabase PostgreSQL with realistic EduPlay demo data for all 6 modules'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚀 Seeding EduPlay Supabase PostgreSQL Database...\n'))

        # ====================================================================
        # MODULE 0: USERS & PROFILES
        # ====================================================================
        users_info = [
            ('admin', 'admin@eduplay.com', 'Super', 'Admin', True, 5000, 10, 15),
            ('alice_dev', 'alice@eduplay.com', 'Alice', 'Sharma', False, 3200, 7, 9),
            ('bob_learn', 'bob@eduplay.com', 'Bob', 'Verma', False, 1850, 4, 5),
            ('carol_code', 'carol@eduplay.com', 'Carol', 'Singh', False, 950, 2, 3),
        ]
        created_users = []
        for username, email, first, last, is_super, xp, level, streak in users_info:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                    'is_staff': is_super,
                    'is_superuser': is_super,
                }
            )
            user.set_password('eduplay123')
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.xp_points = xp
            profile.level = level
            profile.streak_days = streak
            profile.bio = f"Passionate STEM learner exploring EduPlay UnityLearn!"
            profile.save()

            # User analytics
            UserAnalytics.objects.get_or_create(
                user=user,
                defaults={
                    'total_time_spent_hours': round(xp / 120.0, 1),
                    'avg_quiz_score': 85.5,
                    'strongest_subject': 'Computer Science',
                    'weakest_subject': 'Chemistry',
                    'learning_streak': streak,
                }
            )
            created_users.append(user)

        admin_user = created_users[0]
        alice_user = created_users[1]
        self.stdout.write('  ✅ 4 Demo Users ready (admin, alice_dev, bob_learn, carol_code)')

        # ====================================================================
        # MODULE 0 (Gamification): BADGES & USER BADGES
        # ====================================================================
        badges_data = [
            ('First Steps', '🎯', 'Completed first lesson or quiz on EduPlay', 'quiz', 25),
            ('Quiz Wizard', '🏆', 'Achieved 100% score on a competitive quiz', 'quiz', 100),
            ('Lab Pioneer', '🔬', 'Successfully finished 5 physics/bio simulations', 'special', 75),
            ('Streak Master', '🔥', 'Maintained a consecutive 7-day study streak', 'streak', 150),
            ('Knowledge Seeker', '📚', 'Enrolled and completed a comprehensive course', 'course', 200),
            ('Community Hero', '🤝', 'Actively participated in study groups and forums', 'achievement', 50),
            ('Code Architect', '💻', 'Completed all algorithmic coding challenges', 'achievement', 300),
        ]
        badge_objs = []
        for name, icon, desc, btype, xp in badges_data:
            badge, _ = Badge.objects.get_or_create(
                name=name,
                defaults={'icon': icon, 'description': desc, 'badge_type': btype, 'xp_reward': xp}
            )
            badge_objs.append(badge)

        # Assign badges to alice and admin
        for u in [admin_user, alice_user]:
            for b in badge_objs[:4]:
                UserBadge.objects.get_or_create(user=u, badge=b)
        self.stdout.write('  ✅ 7 Badges & initial user achievements seeded')

        # ====================================================================
        # MODULE 1: GAME-BASED LEARNING (Quizzes, Questions, Options)
        # ====================================================================
        categories_data = [
            ('Python & Programming', 'Master core syntax, OOP, and data structures', '#6C63FF', '💻'),
            ('Physics & Mechanics', 'Understand forces, energy, and motion', '#43E97B', '⚛️'),
            ('Calculus & Linear Algebra', 'Vectors, derivatives, and matrix operations', '#FF6584', '📐'),
            ('Web Development', 'Django, APIs, and modern frontend practices', '#FFA726', '🌐'),
        ]
        created_cats = []
        for name, desc, color, icon in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'color': color, 'icon': icon}
            )
            created_cats.append(cat)

        quizzes_seed = [
            {
                'title': 'Python Fundamentals Quest',
                'description': 'Test your Python fundamentals: loops, comprehensions, and data structures.',
                'category': created_cats[0],
                'difficulty': 'easy',
                'time_limit': 15,
                'xp_reward': 150,
                'questions': [
                    {
                        'text': 'Which of the following data structures in Python is immutable?',
                        'points': 10,
                        'explanation': 'Tuples cannot be altered once instantiated.',
                        'options': [
                            ('List', False),
                            ('Tuple', True),
                            ('Dictionary', False),
                            ('Set', False),
                        ]
                    },
                    {
                        'text': 'What is the average time complexity of dictionary lookup in Python?',
                        'points': 15,
                        'explanation': 'Python dictionaries use hash maps giving O(1) average lookup.',
                        'options': [
                            ('O(n)', False),
                            ('O(log n)', False),
                            ('O(1)', True),
                            ('O(n^2)', False),
                        ]
                    },
                    {
                        'text': 'What keyword is used to create a generator in Python?',
                        'points': 15,
                        'explanation': 'The yield keyword turns a standard function into a generator.',
                        'options': [
                            ('return', False),
                            ('yield', True),
                            ('generate', False),
                            ('async', False),
                        ]
                    }
                ]
            },
            {
                'title': "Newton's Laws & Dynamics Challenge",
                'description': 'Solve problems related to force, mass, momentum, and friction.',
                'category': created_cats[1],
                'difficulty': 'medium',
                'time_limit': 20,
                'xp_reward': 200,
                'questions': [
                    {
                        'text': 'What is the formula representing Newton’s Second Law of Motion?',
                        'points': 10,
                        'explanation': 'Net Force equals mass times acceleration (F = m*a).',
                        'options': [
                            ('F = m * a', True),
                            ('E = m * c^2', False),
                            ('P = F / A', False),
                            ('v = u + a * t', False),
                        ]
                    },
                    {
                        'text': 'What is the SI unit of momentum?',
                        'points': 15,
                        'explanation': 'Momentum p = m * v, giving kg·m/s.',
                        'options': [
                            ('Newton (N)', False),
                            ('kg·m/s', True),
                            ('Joule (J)', False),
                            ('Watt (W)', False),
                        ]
                    }
                ]
            },
            {
                'title': 'REST APIs & Architecture Quiz',
                'description': 'Assess your knowledge on HTTP methods, status codes, and JWT auth.',
                'category': created_cats[3],
                'difficulty': 'hard',
                'time_limit': 15,
                'xp_reward': 180,
                'questions': [
                    {
                        'text': 'Which HTTP status code indicates successful resource creation?',
                        'points': 10,
                        'explanation': '201 Created indicates the requested resource was created.',
                        'options': [
                            ('200 OK', False),
                            ('201 Created', True),
                            ('204 No Content', False),
                            ('301 Moved Permanently', False),
                        ]
                    },
                    {
                        'text': 'What header is typically used to transmit a JWT Bearer token?',
                        'points': 15,
                        'explanation': 'Authorization: Bearer <token>',
                        'options': [
                            ('Authorization', True),
                            ('Authentication', False),
                            ('Token', False),
                            ('X-Auth-Key', False),
                        ]
                    }
                ]
            }
        ]

        for q_data in quizzes_seed:
            quiz, created = Quiz.objects.get_or_create(
                title=q_data['title'],
                defaults={
                    'description': q_data['description'],
                    'category': q_data['category'],
                    'created_by': admin_user,
                    'difficulty': q_data['difficulty'],
                    'time_limit': q_data['time_limit'],
                    'xp_reward': q_data['xp_reward'],
                    'is_published': True,
                }
            )
            if created:
                for idx, q_info in enumerate(q_data['questions'], start=1):
                    q = Question.objects.create(
                        quiz=quiz,
                        question_text=q_info['text'],
                        question_type='mcq',
                        points=q_info['points'],
                        order=idx,
                        explanation=q_info['explanation'],
                    )
                    for opt_text, is_corr in q_info['options']:
                        Option.objects.create(
                            question=q,
                            option_text=opt_text,
                            is_correct=is_corr,
                        )
        self.stdout.write('  ✅ Quizzes, Questions, and Options seeded')

        # ====================================================================
        # MODULE 2: INTERACTIVE SIMULATIONS
        # ====================================================================
        sim_cat_phys, _ = SimulationCategory.objects.get_or_create(
            name='Physics Laboratory',
            defaults={
                'description': 'Virtual physics experiments with real-time Newtonian calculation',
                'subject': 'Physics',
                'icon': '⚛️',
                'color': '#43E97B'
            }
        )
        sim_cat_circ, _ = SimulationCategory.objects.get_or_create(
            name='Electrical & Electronics',
            defaults={
                'description': 'Simulate circuits, Ohm’s law, and resistor networks',
                'subject': 'Engineering',
                'icon': '⚡',
                'color': '#FFA726'
            }
        )
        sim_cat_bio, _ = SimulationCategory.objects.get_or_create(
            name='Cellular Biology',
            defaults={
                'description': 'Interactive organelles, cellular respiration, and DNA structure',
                'subject': 'Biology',
                'icon': '🧬',
                'color': '#12C2E9'
            }
        )

        sims_list = [
            ("Newton's Second Law Dynamics Lab", "Adjust force (0-100N), mass (1-20kg), and surface friction in a live physics loop.", sim_cat_phys, 'physics', 'easy', 150),
            ("Ohm's Law Virtual Circuit", "Vary voltage and resistance to observe live current flow and lightbulb illumination.", sim_cat_circ, 'electronics', 'easy', 120),
            ("Simple Harmonic Pendulum", "Explore frequency and period across variable rope length and gravitational environments.", sim_cat_phys, 'physics', 'medium', 160),
            ("Eukaryotic Cell Explorer", "Interactive SVG cell anatomy: inspect Mitochondria, Nucleus, Ribosomes, and Golgi.", sim_cat_bio, 'biology', 'easy', 140),
            ("Mathematical Function Plotter", "Visual canvas grapher plotting sin(x), quadratic curves, and polynomials with dynamic amplitude.", sim_cat_phys, 'math', 'medium', 175),
        ]
        for title, desc, scat, stype, diff, xp in sims_list:
            Simulation.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'category': scat,
                    'simulation_type': stype,
                    'difficulty': diff,
                    'instructions': 'Adjust controls on the left panel and observe the real-time telemetry graph.',
                    'content_data': {'default_parameters': {'mass': 5, 'force': 25, 'friction': 0.1}},
                    'xp_reward': xp,
                    'created_by': admin_user,
                }
            )
        self.stdout.write('  ✅ 5 Interactive Simulations seeded')

        # ====================================================================
        # MODULE 3: ADAPTIVE LEARNING PATHS (Subjects, Courses, Lessons)
        # ====================================================================
        subj_cs, _ = Subject.objects.get_or_create(
            name='Computer Science',
            defaults={'description': 'Software architecture, algorithms, and full-stack development', 'icon': '💻', 'color': '#6C63FF'}
        )
        subj_phys, _ = Subject.objects.get_or_create(
            name='Applied Physics',
            defaults={'description': 'Mechanics, electromagnetism, and modern optics', 'icon': '⚛️', 'color': '#43E97B'}
        )

        courses_seed = [
            (
                'Full-Stack Python & Django Mastery',
                'Comprehensive path from Python syntax to enterprise Django REST APIs and JWT security.',
                subj_cs, 'intermediate', 35.0, 'Prof. Arvind Kumar', 800,
                [
                    ('Module 1: Modern Python Foundations', [
                        ('Python Data Structures Deep Dive', 'Lists, tuples, dictionaries, sets, and comprehension patterns.', 30, 25),
                        ('Object-Oriented Design in Python', 'Classes, inheritance, polymorphism, and magic methods.', 45, 30),
                    ]),
                    ('Module 2: Django Architecture & ORM', [
                        ('Django Request-Response Cycle', 'WSGI/ASGI, URLs, Views, Models, and Admin registration.', 40, 30),
                        ('PostgreSQL Integration with Supabase', 'Connecting remote PostgreSQL, running migrations, and connection pooling.', 50, 40),
                    ]),
                    ('Module 3: RESTful APIs & Authentication', [
                        ('DRF Serializers & ViewSets', 'Building clean JSON APIs with pagination, sorting, and validation.', 45, 35),
                        ('JWT Security & Token Rotation', 'Implementing secure SimpleJWT access and refresh workflows.', 40, 35),
                    ]),
                ]
            ),
            (
                'Classical Mechanics & Dynamics',
                'Master vectors, Newton’s laws, conservation of momentum, and rotational kinematics.',
                subj_phys, 'beginner', 20.0, 'Dr. Neha Sen', 600,
                [
                    ('Module 1: Kinematics in One & Two Dimensions', [
                        ('Vectors and Coordinate Systems', 'Vector addition, cross product, and dot product fundamentals.', 30, 20),
                        ('Projectile Motion Analysis', 'Trajectories, flight time, and launch angle optimizations.', 40, 25),
                    ]),
                    ('Module 2: Dynamics & Energy', [
                        ('Work, Energy, and Power', 'Conservative forces, work-kinetic energy theorem, and potential energy.', 45, 30),
                    ]),
                ]
            )
        ]

        for c_title, c_desc, c_subj, c_diff, c_dur, c_inst, c_xp, c_modules in courses_seed:
            course, created = Course.objects.get_or_create(
                title=c_title,
                defaults={
                    'description': c_desc,
                    'subject': c_subj,
                    'difficulty': c_diff,
                    'duration_hours': c_dur,
                    'instructor_name': c_inst,
                    'xp_reward': c_xp,
                    'is_published': True,
                    'created_by': admin_user,
                }
            )
            if created:
                for m_idx, (m_title, lessons) in enumerate(c_modules, start=1):
                    mod = CourseModule.objects.create(
                        course=course,
                        title=m_title,
                        description=f"Core concepts for {m_title}",
                        order=m_idx,
                        duration_minutes=sum(l[2] for l in lessons)
                    )
                    for l_idx, (l_title, l_content, l_dur, l_xp) in enumerate(lessons, start=1):
                        Lesson.objects.create(
                            module=mod,
                            title=l_title,
                            content=l_content,
                            lesson_type='reading',
                            order=l_idx,
                            xp_reward=l_xp,
                        )

            # Enroll student alice
            Enrollment.objects.get_or_create(
                user=alice_user,
                course=course,
                defaults={'progress_percent': 45.0}
            )
        self.stdout.write('  ✅ Courses, Modules, Lessons, and Enrollments seeded')

        # ====================================================================
        # MODULE 4: COLLABORATIVE LEARNING (Study Groups, Forum, Posts)
        # ====================================================================
        groups_list = [
            ('Python & Backend Developers Guild', 'Collaborate on Django projects, code reviews, and API testing.', 'Computer Science'),
            ('Physics Lab Research Circle', 'Discuss simulations, virtual experiments, and homework problems.', 'Applied Physics'),
            ('Competitive Coding Champions', 'Weekly quiz marathons, algorithmic puzzles, and XP leaderboard sprints.', 'Computer Science'),
        ]
        for g_name, g_desc, g_subj in groups_list:
            grp, _ = StudyGroup.objects.get_or_create(
                name=g_name,
                defaults={
                    'description': g_desc,
                    'subject': g_subj,
                    'created_by': admin_user,
                    'max_members': 50,
                    'is_private': False,
                }
            )
            grp.members.add(admin_user, alice_user)

        gen_forum, _ = Forum.objects.get_or_create(
            title='Campus Discussion & Knowledge Exchange',
            defaults={
                'description': 'Open peer-to-peer discussions on STEM topics, troubleshooting, and project ideas.',
                'subject': 'General',
            }
        )

        posts_seed = [
            (
                'How to optimize database queries in Django using select_related()?',
                'When fetching foreign key relationships, using select_related performs SQL joins and eliminates the N+1 problem. Here is how I set it up in our EduPlay quiz endpoints...',
                alice_user
            ),
            (
                'Understanding frictional coefficient in the Newton Simulation',
                'In the simulation page, does static friction exceed kinetic friction at zero velocity? Let’s test the threshold force together.',
                created_users[2]
            )
        ]
        for p_title, p_content, p_author in posts_seed:
            post, p_created = ForumPost.objects.get_or_create(
                forum=gen_forum,
                title=p_title,
                defaults={
                    'content': p_content,
                    'author': p_author,
                    'views': 42,
                }
            )
            if p_created:
                PostComment.objects.create(
                    post=post,
                    author=admin_user,
                    content='Great question! Yes, definitely check the Django debug toolbar or query count to verify the join efficiency.'
                )
        self.stdout.write('  ✅ Study Groups, Community Forum, Posts, and Comments seeded')

        # ====================================================================
        # MODULE 5: PERFORMANCE ANALYTICS (Activity Logs, Daily Progress)
        # ====================================================================
        today = date.today()
        # Seed 7 days of daily progress for alice
        for i in range(7):
            d = today - timedelta(days=i)
            DailyProgress.objects.get_or_create(
                user=alice_user,
                date=d,
                defaults={
                    'lessons_completed': random.randint(1, 4),
                    'quizzes_completed': random.randint(1, 3),
                    'simulations_completed': 1,
                    'xp_earned': random.randint(80, 260),
                    'time_spent_minutes': random.randint(35, 90),
                }
            )

        activity_samples = [
            ('quiz', 'Completed Python Fundamentals Quest', 'Scored 90% and earned 135 XP', 135),
            ('simulation', 'Experimented with Newton’s Second Law', 'Explored force and acceleration sliders', 150),
            ('lesson', 'Studied Django Request-Response Cycle', 'Completed module 2 reading', 30),
            ('badge_earned', 'Unlocked Streak Master Badge', 'Achieved 7 consecutive active study days', 150),
        ]
        for atype, atitle, adesc, axp in activity_samples:
            ActivityLog.objects.get_or_create(
                user=alice_user,
                title=atitle,
                defaults={
                    'activity_type': atype,
                    'description': adesc,
                    'xp_earned': axp,
                }
            )
        self.stdout.write('  ✅ Daily Progress & Activity Logs seeded')

        # ====================================================================
        # MODULE 6: CONTENT AUTHORING & CUSTOMIZATION TOOLS
        # ====================================================================
        ContentTemplate.objects.get_or_create(
            name='Standard 5-Question MCQ Quiz Template',
            defaults={
                'description': 'Pre-formatted structure for quick interactive assessment creation with scoring keys.',
                'template_type': 'quiz',
                'template_data': {
                    'default_passing_score': 60,
                    'time_limit_minutes': 15,
                    'recommended_points_per_q': 20,
                },
                'created_by': admin_user,
                'is_public': True,
                'downloads_count': 18,
            }
        )

        ContentDraft.objects.get_or_create(
            title='Draft: Thermodynamics & Heat Transfer Lab Guide',
            defaults={
                'content_type': 'article',
                'author': admin_user,
                'status': 'draft',
                'content_data': {
                    'outline': ['Conduction', 'Convection', 'Radiation', 'Carnot Efficiency'],
                    'notes': 'Add interactive temperature differential graph before publishing.',
                }
            }
        )

        CustomQuizBuilder.objects.get_or_create(
            title='Discrete Mathematics Logic Mini-Test',
            defaults={
                'instructions': 'Answer all propositions on truth tables and boolean algebra.',
                'passing_score': 70,
                'time_limit': 10,
                'questions_data': [
                    {
                        'question': 'What is the negation of (P AND Q)?',
                        'options': ['(NOT P) OR (NOT Q)', '(NOT P) AND (NOT Q)', 'P OR Q', 'NOT (P OR Q)'],
                        'correct_index': 0
                    }
                ],
                'created_by': admin_user,
                'is_published': True,
            }
        )
        self.stdout.write('  ✅ Content Authoring Templates, Drafts, and Custom Quizzes seeded')

        self.stdout.write(self.style.SUCCESS('\n🎉 Supabase PostgreSQL database successfully seeded with full EduPlay content!'))
        self.stdout.write(self.style.WARNING('\n🔑 Credentials to Log In:'))
        self.stdout.write('   • Admin User:   admin     / eduplay123')
        self.stdout.write('   • Student User: alice_dev / eduplay123')
        self.stdout.write('   • Student User: bob_learn / eduplay123\n')
