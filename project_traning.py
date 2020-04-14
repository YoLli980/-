from flask import Flask, request, url_for, render_template, flash,redirect,make_response
from exts import db
from  module import  Student , Teacher,Class_known ,Proficiency,Schedule,Curricula,Tmp_Curricula,Surper_root
import config
from flask import Flask
from datetime import datetime
import re
from os import path
from flask_moment import Moment
import datetime
import random,os,filestore,files
from werkzeug.utils import secure_filename
import xlrd

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
Moment(app)
lg_id = 0
lg_stu_id =0

count=0
now_year=datetime.datetime.now().year
last_year =now_year-1
the_last_before_last=now_year-2
stu_sch=[]
tmp_name=""
tmp_grade=""



# 主界面
@app.route('/',methods=['GET','POST'])
def home():

    if request.method == 'POST':
        login_id = request.form.get('inputEmail3')
        login_password = request.form.get('inputPassword3')
        login_radio = request.form.get('inlineRadioOptions')

        if login_radio == 'teacher':
            true_id = Teacher.query.filter_by(num=login_id).first()
            if true_id:
                if true_id.password == login_password:

                    global lg_id
                    lg_id= true_id.id
                    return redirect(url_for('teacher_ui'))
                else:
                    flash('密码有误')
            else:
                flash('没有该用户')
        elif login_radio == 'student':
            true_id = Student.query.filter_by(num=login_id).first()
            if true_id:
                if true_id.password ==login_password:
                    global  lg_stu_id
                    lg_stu_id = true_id.id
                    print('密码正确')
                    return  redirect(url_for('student_ui',login_id=true_id.num))
                else:
                    flash('密码有误')
            else :
                flash('没有该用户')
        elif login_radio == 'others':
            true_id = Surper_root.query.filter_by(num=login_id).first()
            if true_id:
                if true_id.password == login_password:
                    print('密码正确')
                    return redirect(url_for('surper_root_teacher', page=1))
                else:
                    flash('密码有误')
            else:
                flash('没有该用户')

    return render_template('login.html')


# 管理员用户登录
@app.route('/root/',methods=['GET','POST'])
def root():
    return render_template('term_show.html')


#管理员教师信息查看
@app.route('/teacher/<page>')
def root_show_teacher(page):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    teacher_all = Teacher.query.paginate(int(page), 10)
    return render_template('root_show_teacher.html', teacher_all=teacher_all,login_id=login_id,schedule=schedules,teacher_info = teacher_info)
#管理员学生信息查看
@app.route('/student/<page>')
def root_show_student(page):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    stduent_all = Student.query.paginate(int(page),10)
    return render_template('root_show_student.html', stduent_all=stduent_all,login_id=login_id,schedule=schedules,teacher_info = teacher_info)



# 添加教师
@app.route('/add_teacher/',methods=['POST','GET'])
def add_teacher():
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    if request.method == 'POST':
        teacher_id = request.form.get('id')
        teacher_id1 = int(teacher_id)
        teacher_name = request.form.get('name')
        teacher_colleage = request.form.get('department')
        teacher_password = request.form.get('password')
        teacher_password1 = request.form.get('password1')

        if teacher_password == teacher_password1:
            true_id = Teacher.query.filter_by(num=teacher_id1).first()
            if true_id:
                flash('该用户已经存在')
            else:
                try:
                    with app.app_context():
                        new_teacher = Teacher(num=teacher_id1, name=teacher_name, college=teacher_colleage,
                                              password=teacher_password)
                        db.session.add(new_teacher)
                        db.session.commit()

                        flash("教师添加成功")
                        return redirect(url_for('add_teacher',login_id=login_id, schedule=schedules,
                                               teacher_info=teacher_info))
                except Exception as e:
                    db.session.rollback()
                    db.session.commit()
                    flash('添加用户失败,请正确填写用户信息')
        else:
            flash('密码有误')

    return render_template('add_teacher.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)

# 添加学生
@app.route('/add_student/',methods=['GET','POST'])
def add_student():
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    if request.method == 'POST':
        student_id = request.form.get('id')
        student_name = request.form.get('name')
        student_major = request.form.get('major')
        student_password = request.form.get('password')
        student_password1 = request.form.get('password1')

        student_department = request.form.get('department')
        student_grade = request.form.get('grade')


        if student_password == student_password1:
            true_id = Student.query.filter_by(num=student_id).first()
            if true_id:
                flash('该用户已经存在')
            else:
                try:
                    with app.app_context():
                        new_student = Student(num=student_id, name=student_name, major = student_major,grade=student_grade
                            ,college = student_department,password=student_password)
                        db.session.add(new_student)
                        db.session.commit()
                        flash("学生添加成功")
                        return redirect(url_for('add_student', login_id=login_id, schedule=schedules,
                                               teacher_info=teacher_info))
                except Exception as e:
                    db.session.rollback()
                    db.session.commit()
                    flash('添加用户失败')
        else:
            flash('密码有误')
    return render_template('add_student.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)


# 学生UI
@app.route('/student_ui/<login_id>',methods=['GET','POST'])
def student_ui(login_id):
    global now_year,last_year,the_last_before_last
    now_year=datetime.datetime.now().year
    last_year =now_year-1
    the_last_before_last=now_year-2
    print("now_year",now_year)
    print("last_year",last_year)
    print("the_last_before_last",the_last_before_last)
    print(type(now_year))
    int(lg_stu_id)

    global  stu_sch
    stu_sch = []

    stu_id = Student.query.filter_by(id=lg_stu_id).first()
    stu_sch_all = stu_id.curricula
    for stu in stu_sch_all:
        s = Schedule.query.get(stu.schedule_id)
        stu_sch.append(s)

    return render_template('student_ui.html',student_info=stu_id,schedule_all=stu_sch,now_year=now_year,
                           last_year=last_year,last_year_before=the_last_before_last)


#删除教师
@app.route('/teacher_delete/',methods=['GET','POST'])
def teacher_delete():
    teacher_id=request.form.get('de_teacher')
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    print("tea",teacher)
    with app.app_context():
        try:
            print("dfa")
            db.session.delete(teacher)
            Schedule.query.filter(Schedule.teacher_id == None).delete()
            db.session.commit()
        except Exception as e:
            print("删除教师失败")
    return "删除成功"

#删除学生
@app.route('/student_delete/',methods=['GET','POST'])
def student_delete():
    student_id = request.form.get('rm_student')

    with app.app_context():
        try:
            Student.query.filter_by(id=int(student_id)).delete()
            db.session.commit()
        except Exception as e:
            print("删除学生失败")

    return "hello"




# 课程录入
@app.route('/schedule/',methods=['GET','POST'])
def schedule():
    teacher_id = lg_id
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    # schedule_id = request.form.get('id')
    schedule_name = request.form.get('name')
    schedule_time = request.form.get('grade')
    major = request.form.get('major')
    classes = request.form.get('classes')
    schedule_colleage = request.form.get('college')

    if request.method == "POST":
        rand_core = (random.randint(100000, 800000))
        str(rand_core)
        if schedule_name and schedule_time and schedule_colleage:
            with app.app_context():
                try:
                    schedule_add = Schedule(name=schedule_name, grade=schedule_time, college=schedule_colleage,
                                            teacher_id=teacher_id,random_code=rand_core,major=major,classes=classes)
                    db.session.add(schedule_add)
                    db.session.commit()
                    return redirect(url_for('schedule_ui'))
                except:
                    db.session.rollback()
                    db.session.commit()
                    flash('导入失败')
        else:
            flash('数据不能为空')

    return render_template('add_schedule.html',now_year=now_year,
                           last_year=last_year,last_year_before=the_last_before_last,
                           login_id=login_id,schedule=schedules,teacher_info = teacher_info)


# 教师课程UI
@app.route('/schedule_ui/',methods=['GET','POST'])
def schedule_ui():
    class_points=[]
    teacher = Teacher.query.filter_by(id=lg_id).first()
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule


    schedule_show = teacher.schedule

    return render_template('schedule_show.html',schedule_shows=schedule_show,teacher=teacher,
                           login_id=login_id,schedule=schedules,teacher_info = teacher_info)


# 知识点录入
@app.route('/konw_point/<schedule_id>',methods=['GET','POST'])
def know_point(schedule_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    teacher=Teacher.query.get(int(lg_id))
    schedule = Schedule.query.get(schedule_id)
    print("schedule.id",schedule.id)
    class_points=schedule.class_point
    new_title = request.form.get('name')
    print("id1", new_title)
    if request.method == 'POST':

        new_title=request.form.get('name')
        print("id",new_title)
        true_title = Class_known.query.filter_by(name=new_title).first()

        if true_title :
            flash('已经存在相同知识点内容')
        else:
            with app.app_context():
                try:
                    add_konw=Class_known(name =new_title,schedule_id=schedule_id)
                    db.session.add(add_konw)
                    db.session.commit()
                    # return redirect(url_for('teacher_ui'))
                    return redirect(url_for('schedule_ui'))
                except:
                    db.session.rollback()
                    db.session.commit()

    return render_template('add_know_point.html',class_points=class_points,teacher=teacher,login_id=login_id,schedule=schedules,teacher_info = teacher_info)




# 学生个人中心
@app.route('/student_Per_info/')
def person_info():

    true_no_comments = []
    lg_stu_id1 = int(lg_stu_id)
    global now_year, last_year, the_last_before_last
    now_year = datetime.datetime.now().year
    last_year = now_year - 1
    the_last_before_last = now_year - 2

    print(type(now_year))
    int(lg_stu_id)

    global stu_sch
    stu_sch = []

    stu_id = Student.query.filter_by(id=lg_stu_id).first()
    stu_sch_all = stu_id.curricula
    for stu in stu_sch_all:
        s = Schedule.query.get(stu.schedule_id)
        stu_sch.append(s)

    schedule_all = []
    student_info = Student.query.get(int(lg_stu_id))
    stu_cur=Curricula.query.filter_by(student_id=int(lg_stu_id)).all()
    for i in stu_cur:
        schedule=Schedule.query.get(i.schedule_id)
        schedule_all.append(schedule)
    return  render_template('student_pro_info.html',true_no_comments=true_no_comments,stu=stu_id,
                               student_info=student_info,schedule_all=stu_sch,now_year=now_year,
                           last_year=last_year,last_year_before=the_last_before_last,
                            stu_cur=schedule_all,)

#学生个人修改密码
@app.route("/stu_paw_change/",methods=['GET','POST'])
def stu_paw_change():
    if request.method=="POST":
        password = request.form.get("password")
        password1 = request.form.get("password1")
        print("password",password,password1)

        if password and password1:
            with app.app_context():
                try:
                    stu=Student.query.get(lg_stu_id)
                    stu.password = password
                    db.session.commit()
                    return  render_template('login.html')
                except:
                    db.session.rollback()
                    db.session.commit()
                    flash("密码修改失败请核对后再修改")
        else:
            flash("两次密码不一样")

    return redirect(url_for('person_info'))

# 教师个人中心
@app.route('/teacher_Per_info/')
def teacher_Per_info():
    teacher_info=Teacher.query.get(int(lg_id))
    tea_schedule=teacher_info.schedule

    return render_template('teacher_pro_info.html',teacher_info=teacher_info,tea_schedule=tea_schedule)

# 教师个人密码修改
@app.route("/tea_paw_change/",methods=['GET','POST'])
def tea_paw_change():
    if request.method=="POST":
        pass_word=request.form.get("password")
        pass_word1=request.form.get("password1")
        print("pass_word,pass_word1",pass_word,pass_word1)
        if pass_word and pass_word1:
            with app.app_context():
                try:
                    teacher=Teacher.query.get(int(lg_id))
                    teacher.password = pass_word
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.commit()

        else:
            flash("请输入正确的密码")
    return redirect(url_for('teacher_Per_info'))


# 教师知识点展示
@app.route('/kown_ui/<schedule_id>',methods=['GET','POST'])
def kown_point_ui(schedule_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    # 通过教师的ID获得所有课程
    teacher = Teacher.query.get(int(lg_id))
    # schedules=teacher.schedule

    schedule_info = Schedule.query.get(schedule_id)

    if schedule_info:
        class_point_all=schedule_info.class_point

    if class_point_all:
        return render_template('konw_show.html',class_point_all=class_point_all,schedule_info_name=schedule_info.name
        ,teacher=teacher,login_id=login_id,schedule=schedules,teacher_info = teacher_info)
    return "没有知识点"

# 修改知识点
@app.route('/chang_konw/<class_konw_id>',methods=['GET','POST'])
def chang_konw(class_konw_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    teacher = Teacher.query.get(int(lg_id))

    class_konw = Class_known.query.get(class_konw_id)
    new_title = request.form.get('name')
    if request.method == 'POST':
        if new_title:

            if Class_known.query.filter_by(name=new_title).first():
                flash('已经存在相同知识点内容')
            else:
                with app.app_context():
                    try:
                        add_konw = class_konw.name = new_title
                        db.session.commit()
                        return redirect(url_for('schedule_ui'))
                    except:
                        db.session.rollback()
                        db.session.commit()
        else:
            flash('请输入知识点')

    return render_template('change_konw.html',teacher=teacher,login_id=login_id,schedule=schedules,teacher_info = teacher_info)


#修改课程
@app.route('/schedule_change/<schedule_id>',methods=['GET','POST'])
def schedule_change(schedule_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    teacher = Teacher.query.get(int(lg_id))
    name = request.form.get('name')
    classes = request.form.get('classes')
    major = request.form.get('major')
    grade = request.form.get('grade')
    college = request.form.get('college')

    new_schedule_id = int(schedule_id)
    schedule_c = Schedule.query.get(new_schedule_id)
    if request.method == "POST":
        with app.app_context():
            try:
                # schedule_add = Schedule(name=schedule_name, term=schedule_time, college=schedule_colleage,
                #                         teacher_id=teacher_id)
                # db.session.add(schedule_add)

                schedule_c.name = name
                schedule_c.major = major
                schedule_c.classes = classes
                schedule_c.grade = grade
                schedule_c.college = college
                db.session.commit()
                return redirect(url_for('schedule_ui'))
            except:
                db.session.rollback()
                db.session.commit()
                flash('修改失败')

    return render_template('schedule_change.html',schedule_c=schedule_c,now_year=now_year,
                           last_year=last_year,last_year_before=the_last_before_last,teacher=teacher,login_id=login_id,schedule=schedules,teacher_info = teacher_info)



# 教师UI
@app.route('/teacher_ui/',methods=['GET','POST'])
def teacher_ui():
    login_id =lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    return render_template('teacher_ui.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)


#学生评价反馈导入数据库
@app.route('/student_feedback/',methods=['GET','POST'])
def student_feedback():
    se_radio = request.form.get("radio_name")
    se_content = request.form.get("content")
    kown_id = request.form.get("kown_id")
    if request.method == "POST":
        if se_radio and se_content and kown_id:
            proficiency_all=Proficiency.query.filter_by(proficiency=se_radio,estimate=se_content,class_know_id=kown_id,student_id=lg_stu_id).first()
            if proficiency_all :
                flash("换个评论吧大侠")
                print("换个评论吧大侠")
            else:
                with app.app_context():
                    try:
                        new_proficiency = Proficiency(proficiency=se_radio,estimate=se_content,student_id=lg_stu_id,class_know_id=kown_id)
                        db.session.add(new_proficiency)
                        db.session.commit()
                        print("录入成功")
                    except Exception as e:
                        db.session.rollback()
                        db.session.commit
        else:
            flash("送上你的评论吧")
    return "hello"


# 教师端获得学生评价信息
@app.route('/get_stu_feback/<class_konw_id>')
def get_stu_feback(class_konw_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    # A,B,C分别代表：全掌握，基本掌握，未掌握
    class_konw_all= Class_known.query.get(class_konw_id)
    proficiency_all=class_konw_all.proficiency
    class_konw_all_name=class_konw_all.name

    schedule_id=class_konw_all.schedules.id
    count=Curricula.query.filter_by(schedule_id=int(schedule_id)).count()

    # for i in proficiency_all:
    #     print("掌握情况",i.proficiency)
    #     print("评论",i.estimate)
    # 通过知识点ID查看掌握情况 ,sh_pat： 掌握 ，partly_mastered ：部分掌握掌握，unfinished:未掌握
    A=Proficiency.query.filter(Proficiency.class_know_id==class_konw_id).filter(Proficiency.proficiency == "全掌握").count()
    B=Proficiency.query.filter(Proficiency.class_know_id==class_konw_id).filter(Proficiency.proficiency == "基本掌握").count()
    C=Proficiency.query.filter(Proficiency.class_know_id==class_konw_id).filter(Proficiency.proficiency == "未掌握").count()

    sum = A+B+C

    return render_template('bingzhuangtu.html',A=A,B=B,C=C,count=count
                           ,sum=sum,proficiency_all_name=class_konw_all_name,login_id=login_id,schedule=schedules,teacher_info = teacher_info)
# 学生课程列表
# @app.route('/student_schedule/',methods=['GET','POST'])
# def student_schedule():
#
#     # 获得所有课程
#     # stu_sch_all = Curricula.query.filter(Curricula.student_id==lg_stu_id).all
#     #
#     # print(stu_sch_all.id)
#     stu_sch=[]
#     stu_id = Student.query.get(lg_stu_id)
#     stu_sch_all=stu_id.curricula
#     for stu in stu_sch_all:
#         s=Schedule.query.get(stu.schedule_id)
#         stu_sch.append(s)
#     # print(stu_sch)
#     # schedule_all = Schedule.query.all()
#     # 获得所有知识点
#     # for known_id in known_all:
#     #     known_all_list.append(known_id)
#         # print(known_all_list)
#
#     # 通过遍历知识点ID获得所有课程ID
#     # for i in known_all:
#     #     kown_point1 = Class_known.query.get(i.id)
#     #     schedule_list.append(kown_point1.schedules)
#         # print('kown=',i.id)
#     # 通过遍历课程ID获得所有教师ID
#     # for j in schedule_list:
#     #     schedules = Schedule.query.get(j.id)
#     #     teacher_list.append(schedules.teahcers)
#         # print('schedule',j.id ,j.name)
#
#     # for i,j,k in zip(known_all_list,schedule_list,teacher_list):
#     #     # print(i.name,j.name)
#     #     stu_kown_all.append(i.name)
#     #     stu_kown_all.append(i.content)
#     #     stu_kown_all.append(j.name)
#     #     stu_kown_all.append(k.name)
#
#     return  render_template('student_kown.html',schedule_all=stu_sch)




# 学生知识点展示


#学生知识点评论


@app.route('/get_stu_estimate/<class_konw_id>')
def get_stu_estimate(class_konw_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    class_konw_all = Class_known.query.get(class_konw_id)
    estimate=class_konw_all.proficiency
    return render_template('stu_estimate.html',class_konw_all=class_konw_all,login_id=login_id,schedule=schedules,teacher_info = teacher_info)

@app.route('/student_kown/<schedule_id>',methods=['GET','POST'])
def  student_kown(schedule_id):
    have_comments=[]
    no_comments=[]
    new_no_comments=[]
    have_estimate=[]
    have_proficiency=[]
    have_comments1=[]
    new_no_comments_know=[]
    get_pro_all2=[]
    main_list=[]
    ture_pro_id=[]
    stu_sch=[]
    a=[]

    # 没有评论的知识点
    no_main_comments=[]

    # 下面写法比较混乱，大概说一下思路。
    # 1.通过课程查找出所有的知识点
    # 2.再通过所有的知识点找到评价的列表
    # 3.1如果没有找到直接添加没有评论过的知识点的ID赋值给new_no_comment，
    # 3.2 如果能找到评论过的内容，再判断是否当前登录的为该评论的学生。如果是则直接赋值知识点内容。否则再进行判断
    # 4.如果该评论内容不是当前登录学生所评论则把该知识点放在new_no_comments中。
    # 5.将获取到的new_no_comments元素中所包含的模块函数转化为知识点内容 a列表，再和have_comments1进行比较
    # 6.如果have_comments1 中存在a中的元素则不取该元素，剩下的便是没有评论过的知识点

    student_schedules = Schedule.query.get(schedule_id)
    student_kowns = student_schedules.class_point
    print("id",lg_stu_id)
    aa=int(lg_stu_id)
    for h in student_kowns:
        sigle = Class_known.query.get(h.id)
        ture_pro_id = sigle.proficiency

        if ture_pro_id:
            for p in ture_pro_id:
                # get_pro_all = Proficiency.query.filter_by(student_id=lg_stu_id).first()

                # print(get_pro_all.id)
                if p.student_id == aa:
                    have_comments.append(h)

                    have_proficiency.append(p)
                    have_comments1.append(p.class_know_id)
                else:
                    # get_pro_all.class_know_id ==h.id
                    no_comments.append(p.class_know_id)
                    for i in no_comments:
                        # print("a", i)
                        if not i in new_no_comments:
                            new_no_comments.append(i)
        else:
            new_no_comments.append(h)
        for kk in new_no_comments:
            if isinstance(kk, int):
                sigle1 = Class_known.query.get(kk)
                ture_pro_id1 = sigle1.proficiency
                for p1 in ture_pro_id1:
                    # get_pro_all = Proficiency.query.filter_by(student_id=lg_stu_id).first()
                    get_pro_all2 = Proficiency.query.get(p1.id)
                    # print("p1 ",get_pro_all2.id,p1.id)
                    if get_pro_all2.student_id != lg_stu_id:
                        a.append(kk)
            else:
                a.append(kk.id)
    print(lg_stu_id)
    lg_stu_info=Student.query.get(lg_stu_id)
    # 获得最终没有评论的知识点
    main_list = list(set(a) - set(have_comments1))
    print("没有掌握的知识点", main_list)
    for m in main_list:
        aa = Class_known.query.get(m)
        no_main_comments.append(aa)

    print("评论过的内容",have_proficiency)


    stu_id = Student.query.filter_by(id=lg_stu_id).first()
    stu_sch_all = stu_id.curricula
    for stu in stu_sch_all:
        s = Schedule.query.get(stu.schedule_id)
        stu_sch.append(s)



    return render_template('student_kown_show.html',last_year_before=the_last_before_last,
                           now_year=now_year,last_year=last_year,schedule_all=stu_sch,have_proficiency
                           =have_proficiency,
                           student_info=lg_stu_info,have_comments=have_comments,no_comments=no_main_comments)


# 选择课程
@app.route('/<name>/<grade>',methods=['GET','POST'])
def student_selet(name,grade):
    schedule_show = []
    no_comments = []
    have_comments=[]
    main_list = []
    true_no_comments = []
    lg_stu_id1 = int(lg_stu_id)
    global now_year, last_year, the_last_before_last
    now_year = datetime.datetime.now().year
    last_year = now_year - 1
    the_last_before_last = now_year - 2
    # print("now_year",now_year)
    # print("last_year",last_year)
    # print("the_last_before_last",the_last_before_last)
    print(type(now_year))
    int(lg_stu_id)

    global stu_sch
    stu_sch = []

    stu_id = Student.query.filter_by(id=lg_stu_id).first()
    stu_sch_all = stu_id.curricula
    for stu in stu_sch_all:
        s = Schedule.query.get(stu.schedule_id)
        stu_sch.append(s)


    student_info = Student.query.get(lg_stu_id1)
    schedule_all = Schedule.query.filter(Schedule.college == name, Schedule.grade == grade).all()
    print(schedule_all)
    for i in schedule_all:

        # schedule_siger = Schedule.query.get(i.id)
        # curriculas = schedule_siger.tmp_curricula

        true_curr = Curricula.query.filter(Curricula.schedule_id == i.id,
                                           Curricula.student_id == int(lg_stu_id)).first()
        tmp_curr = Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id == i.id,
                                              Tmp_Curricula.student_id == int(lg_stu_id)).first()
        if true_curr or tmp_curr:
            continue
        else:
            true_no_comments.append(i)

    #     if curriculas:
    #         for j in curriculas:
    #             if j.student_id == lg_stu_id1:
    #                 print("i,j", i, j)
    #                 have_comments.append(i.id)
    #             else:
    #                 no_comments.append(i.id)
    #     else:
    #         no_comments.append(i.id)
    # # 消除相同的课程
    # main_list = list(set(no_comments) - set(have_comments))

    # 通过ID获得该课程的信息
    # for kk in main_list:
    #     a = Schedule.query.get(kk)
    #     true_no_comments.append(a)


    # 选择课程
    radio_id = request.values.getlist("s_option")

    for i in radio_id:
        new_i = int(i)
        s_exit = Schedule.query.get(new_i)
        true_cu = Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id == s_exit.id,
                                             Tmp_Curricula.student_id == lg_stu_id1).first()
        if true_cu:
            flash('不要重复选择课程')
        else:
            with app.app_context():
                try:
                    curr = Tmp_Curricula(schedule_id=s_exit.id, student_id=lg_stu_id1)
                    db.session.add(curr)
                    db.session.commit()
                    global count
                    count += 1
                    return redirect(url_for('add_student', login_id=login_id, schedule=schedules,
                                            teacher_info=teacher_info))
                except:
                    db.session.rollback()
                    flash('选课失败，请稍后重试')


    if count == 0:
        return render_template('select_schedule.html', true_no_comments=true_no_comments,stu=stu_id,
                               student_info=student_info,schedule_all=stu_sch,now_year=now_year,
                           last_year=last_year,last_year_before=the_last_before_last)
    else:
        count = 0
        return redirect(url_for('rand_core',true_no_comments=true_no_comments,student_info=student_info))


# 验证课程码
@app.route("/rand_core/",methods=["GET","POST"])
def rand_core():

    tmp_schedule_id=[]
    ture_schedule_id=[]
    stu_sch1=[]
    main_list=[]
    ture_main=[]
    student_info = Student.query.get(int(lg_stu_id))
    tmp_Curricula = Tmp_Curricula.query.filter_by(student_id=lg_stu_id).all()
    for i in tmp_Curricula:
        tmp_schedule_id.append(i.schedule_id)


    ture_Curricula=Curricula.query.filter_by(student_id=lg_stu_id).all()
    for j in  ture_Curricula:
        ture_schedule_id.append(j.schedule_id)


    main_list = list(set(tmp_schedule_id) - set(ture_schedule_id))

    print("main_list",main_list)
    for s in main_list:
        ture_main.append(Schedule.query.get(s))

    # for j in tmp_schedule:
    #     print("schedule_name schedule_college",j.name,j.college)
    if request.method == "POST":
        tmp_rand_core = request.form.get("tmp_rand_core")
        tmp_schedule_id = request.form.get("tmp_schedule_id")
        int(tmp_schedule_id)
        str(tmp_rand_core)
        print("tmp_rand_core" ,tmp_rand_core)
        print("tmp_schedule_id",tmp_schedule_id)
        if tmp_rand_core and tmp_schedule_id:
            ture_schedule=Schedule.query.filter(Schedule.id==tmp_schedule_id,Schedule.random_code==tmp_rand_core).first()
            print("ture_schedule",ture_schedule)
            if ture_schedule:
                with app.app_context():
                    try:
                        ture_curricula=Curricula(schedule_id=ture_schedule.id,student_id=int(lg_stu_id))
                        Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id==ture_schedule.id,Tmp_Curricula.student_id==int(lg_stu_id)).delete()
                        db.session.add(ture_curricula)
                        db.session.commit()
                        print("选课成功")
                        return "sucess"
                    except :
                        db.session.rollback()
                        db.session.commit()
            else:
                flash('验证码错误！')
                print("验证码错误")

    stu_id = Student.query.filter_by(id=lg_stu_id).first()
    stu_sch_all = stu_id.curricula
    for stu in stu_sch_all:
        s = Schedule.query.get(stu.schedule_id)
        stu_sch1.append(s)

    return render_template('select_schedule_new.html', tmp_schedule=ture_main,lg_stu_id=lg_stu_id,student_info=student_info,
                           now_year=now_year,schedule_all=stu_sch1,
                           last_year=last_year, last_year_before=the_last_before_last
                           )


# 教师端查看某个课程的所有知识点反馈信息
@app.route('/teacher_schedule_all/<schedule_id>',methods=['GET','POST'])
def teacher_schedule_all(schedule_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    # A,B,C,分别代表，掌握，基本掌握，未掌握

    kown_name_all=[]
    A=[];B=[];C=[]
    sum_all=[]
    results=[]
    A_sum=0
    B_sum=0
    C_sum=0

    sch = Schedule.query.get(int(schedule_id))
    # 该课程的所有知识点
    konw_all=sch.class_point
    for class_konw in konw_all:
        A1 = Proficiency.query.filter(Proficiency.class_know_id == class_konw.id).filter(
            Proficiency.proficiency == "全掌握").count()
        B1 = Proficiency.query.filter(Proficiency.class_know_id == class_konw.id).filter(
            Proficiency.proficiency == "基本掌握").count()
        C1 = Proficiency.query.filter(Proficiency.class_know_id == class_konw.id).filter(
            Proficiency.proficiency == "未掌握").count()

        sum = A1 + B1 + C1
        kown_name_all.append(class_konw.name)

        A.append(A1)
        B.append(B1)
        C.append(C1)
        sum_all.append(sum)

    for i,j,k in zip(A,B,C):
        A_sum+=i
        B_sum+=j
        C_sum+=k

    print("A,B,C",A_sum,B_sum,C_sum)

    return render_template('student_feedback_bzt.html',kown_name=kown_name_all,A=A,
    B=B,C=C,sum_all=sum_all,sch=sch,A_sum=A_sum,B_sum=B_sum,C_sum=C_sum,login_id=login_id,schedule=schedules,teacher_info = teacher_info)


#某个课程的学生列表
@app.route('/tea_student_show/<schedule_id>',methods=['GET','POST'])
def tea_student_show(schedule_id):

    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    student=[]
    curr = Curricula.query.filter_by(schedule_id=int(schedule_id)).all()
    for i in curr:
        student.append(Student.query.get(i.student_id))
    print(student)
    return render_template('student_show.html',student=student,
                           login_id=login_id,schedule=schedules,teacher_info = teacher_info)

#将学生踢出班级
@app.route('/kick_out_stu/',methods=['GET','POST'])
def kick_out_stu():

    if request.method == 'POST':
        stu_id = request.form.get('stu_id')
        print("stu_id",stu_id)
        with app.app_context():
            try:
                Curricula.query.filter_by(student_id=int(stu_id)).delete()

                db.session.commit()
            except:
                db.session.rollback()
                db.session.commit()

    return "hello"


# 删除知识点
# @app.route("/class_konw_delete/<class_konw_id>",methods=['GET','POST'])
# def class_konw_delete(class_konw_id):
#     class_know=Class_known.query.filter_by(id=class_konw_id).first()
#     schedule_id=class_know.schedules.id
#     # 删除该知识点的所有的评论再删除
#     with app.app_context():
#         try:
#             db.session.delete(class_know)
#             Proficiency.query.filter_by(class_know_id=None).delete()
#             db.session.commit()
#         except Exception as e:
#             flash("删除失败")
#
#
#     # if class_know:
#     #     with app.app_context():
#     #         try:
#     #                 # 删除评论
#     #                 Proficiency.query.filter_by(class_kown=class_know).delete()
#     #                 # 删除作者
#     #                 db.session.delete(class_know)
#     #                 db.session.commit()
#     #
#     #         except:
#     #             db.session.rollback()
#     #             db.session.commit()
#     #             flash("删除失败")
#
#     return redirect(url_for('kown_point_ui',schedule_id=schedule_id))
#     # return "success"

# 期末评教
@app.route("/end_feedback/")
def end_feedback():
    print("gdsa",lg_stu_id)
    a=[]
    schedules=[]
    teacher_name = []
    main_list=[]
    currs = Curricula.query.filter_by(student_id=lg_stu_id).all()

    for i in currs:
        a.append(i.schedule_id)
    print(a)
    for j in a:
        schedule_a =Schedule.query.get(int(j))
        # teacher_name.append(schedule_a.teahcers.name)

        # schedules.append(schedule_a)


    #     main_list.append(schedule_a)
    #     main_list.append(schedule_a.teahcers)
    #
    #
    #
    # print(schedules)
    # print(teacher_name)
    # print(main_list)
    # tuple(main_list)
    # print(main_list[0].name)
    # print(main_list[1])

    # , teacher_name = teacher_name
    return render_template('end_feedback.html',schedules=schedules)


# 查询
@app.route('/find/',methods=['GET','POST'])
def find():
    tea_schedule=[]
    tea_schedule1=[]
    true_schedule =[]
    count = 0;
    if request.method=="POST":
        name=request.form.get("input_name","")
        teacher_name=Teacher.query.filter(Teacher.name.contains(name)).all()
        schedule_name=Schedule.query.filter(Schedule.name.contains(name)).all()

        print("teacher_name",teacher_name)
        print("schedule_name",schedule_name)

        student_info = Student.query.get(int(lg_stu_id))
        for j in schedule_name:
            true_curr = Curricula.query.filter(Curricula.schedule_id == j.id,
                                               Curricula.student_id == int(lg_stu_id)).first()
            tmp_curr = Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id == j.id,
                                                  Tmp_Curricula.student_id == int(lg_stu_id)).first()
            if true_curr or tmp_curr:
                continue
            else:
                true_schedule.append(j)


        for i in teacher_name:
            sc = i.schedule    #获取课程
            for j in sc:

                true_curr = Curricula.query.filter(Curricula.schedule_id == j.id,Curricula.student_id== int(lg_stu_id)).first()
                tmp_curr = Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id == j.id,Tmp_Curricula.student_id== int(lg_stu_id)).first()
                if true_curr or tmp_curr:
                    continue
                else:
                    tea_schedule.append(j)

        print("tea_schedule",tea_schedule)
        print("true_schedule", true_schedule)

        return render_template('find.html',schedule_name=true_schedule,teacher_name=tea_schedule,
        student_info=student_info ,last_year_before=the_last_before_last,schedule_all=stu_sch,
            now_year=now_year,last_year=last_year )
    return "页面跑丢了"


# 查询处理
@app.route('/find/deal_with/',methods=['GET','POST'])
def find_dealwith():
    print("学生ID",lg_stu_id)
    if request.method == 'POST':
        ched = request.values.getlist('s_option') #返回课程ID
        print('ched', ched)
        for i in ched:
            tmp_cur = Tmp_Curricula.query.filter(Tmp_Curricula.schedule_id == int(i),Tmp_Curricula.student_id==int(lg_stu_id)).first()
            if tmp_cur:
                continue
            else:
                with app.app_context():
                    try:
                        tmp_sch = Tmp_Curricula(schedule_id = int(i),student_id = int(lg_stu_id))
                        db.session.add(tmp_sch)
                        db.session.commit()
                        print("ok",i)
                    except:
                        db.session.rollback()
                        db.session.commit()
        return    redirect(url_for('rand_core'))

    return "hello"

# 管理员查询
@app.route('/root_find/',methods=['GET','POST'])
def root_find():
    tea_name = []
    stu_name= []
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    if request.method=="POST":
        name=request.form.get("input_name","")
        teacher_name=Teacher.query.filter(Teacher.name.contains(name)).all()
        student_name=Student.query.filter(Student.name.contains(name)).all()
    else:
        return "错误"
    for i in teacher_name:
        tea_name.append(i)

    for j in student_name:
        stu_name.append(j)

    return render_template('root_find.html',teacher_name=tea_name,student_name=stu_name,login_id=login_id,schedule=schedules,teacher_info = teacher_info)



# 管理员教师修改
@app.route('/teacher_change/<teacher_id>',methods=['GET','POST'])
def teacher_change(teacher_id):
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    teacher_all = Teacher.query.get(teacher_id)

    if request.method == "POST":

        teacher_id1 = int(teacher_id)
        teacher_num = request.form.get('id')
        teacher_name = request.form.get('name')
        teacher_colleage = request.form.get('department')
        teacher_password = request.form.get('password')
        teacher_password1 = request.form.get('password1')

        if teacher_password and teacher_password1:
            with app.app_context():
                try:
                    teacher_all.num=teacher_num
                    teacher_all.name=teacher_name
                    teacher_all.college=teacher_colleage
                    teacher_all.password=teacher_password
                    db.session.commit()
                    return redirect(url_for('root_show_teacher',page=1))
                except:
                    db.session.rollback()
                    db.session.commit()
        print("teacher_id1,teacher_name,teacher_colleage,teacher_password",teacher_id1,teacher_name,teacher_colleage,teacher_password)

    return render_template('teacher_change.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)



# 超级管理员教师修改
@app.route('/root_teacher_change/<teacher_id>',methods=['GET','POST'])
def root_teacher_change(teacher_id):


    teacher_all = Teacher.query.get(teacher_id)

    if request.method == "POST":

        teacher_id1 = int(teacher_id)
        teacher_num = request.form.get('id')
        teacher_name = request.form.get('name')
        teacher_colleage = request.form.get('department')
        teacher_password = request.form.get('password')
        teacher_password1 = request.form.get('password1')

        if teacher_password and teacher_password1:
            with app.app_context():
                try:
                    teacher_all.num=teacher_num
                    teacher_all.name=teacher_name
                    teacher_all.college=teacher_colleage
                    teacher_all.password=teacher_password
                    db.session.commit()
                    return redirect(url_for('surper_root_teacher',page=1))
                except:
                    db.session.rollback()
                    db.session.commit()
    return render_template('surper_teacher_change.html',teacher_info = teacher_all)


# 超级管理员学生修改
@app.route('/root_student_change/<student_id>',methods=['GET','POST'])
def root_student_change(student_id):

    if request.method == 'POST':
        student_num = request.form.get('id')
        student_name = request.form.get('name')
        student_major = request.form.get('major')
        student_password = request.form.get('password')
        student_password1 = request.form.get('password1')
        student_department = request.form.get('department')
        student_grade = request.form.get('grade')

        if student_password == student_password1:
            true_id = Student.query.filter_by(id=student_id).first()
            if true_id:
                try:
                    with app.app_context():
                        true_id.num = int(student_num)
                        true_id.name = student_name
                        true_id.major = student_major
                        true_id.grade = student_grade
                        true_id.college = student_department
                        true_id.password = student_password
                        db.session.commit()
                        return redirect(url_for('surper_root_student', page=1))
                        flash("学生修改成功")
                except Exception as e:
                    db.session.rollback()
                    db.session.commit()
                    flash('修改用户失败')
        else:
            flash('密码有误')

    return  render_template('surper_student_change.html')


# 管理员学生信息修改
@app.route('/student_change/<student_id>',methods=['GET','POST'])
def student_change(student_id):

    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    if request.method == 'POST':
        student_num = request.form.get('id')
        student_name = request.form.get('name')
        student_major = request.form.get('major')
        student_password = request.form.get('password')
        student_password1 = request.form.get('password1')
        student_department = request.form.get('department')
        student_grade = request.form.get('grade')


        if student_password == student_password1:
            true_id = Student.query.filter_by(id=student_id).first()
            if true_id:
                try:
                    with app.app_context():
                        true_id.num = int(student_num)
                        true_id.name = student_name
                        true_id.major = student_major
                        true_id.grade = student_grade
                        true_id.college = student_department
                        true_id.password = student_password
                        db.session.commit()
                        return redirect(url_for('root_show_student',page=1))
                        flash("学生修改成功")
                except Exception as e:
                    db.session.rollback()
                    db.session.commit()
                    flash('修改用户失败')
        else:
            flash('密码有误')



    return render_template('student_change.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)



@app.route('/export_excel')
def export_excel():
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule
    return  render_template('export_excel.html',login_id=login_id,schedule=schedules,teacher_info = teacher_info)


# 导入Excel表格
@app.route('/root/add_excel/', methods=['POST'])
def add_excel():
    student = []
    file = request.files["bookimage"]
    # base_path = path.abspath(path.dirname(__file__))
    # upload_path = path.join(base_path, 'static/uploads/')
    # file_name = upload_path + secure_filename(f.filename)
    # f.save(file_name)

    f = file.read()  # 文件内容
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字
    print(names)
    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕


    nrows = table.nrows  # 获取该sheet中的有效行数
    ncols = table.ncols  # 获取该sheet中的有效列数


    student_info = data.sheet_by_name("学生信息")
    tea_info = data.sheet_by_name("教师信息")

    # 导入学生信息
    stu_nrows = student_info.nrows
    for i in range(stu_nrows):
        if i == 0:
            continue
        student_row = student_info.row_values(i)
        num = int(student_row[0])
        name = student_row[1]
        major = student_row[2]
        grade = student_row[3]
        college = student_row[4]
        password = int(student_row[5])
        # print(num, name, major, grade, college,password)
        ex_stu=Student.query.filter_by(num=num).first()
        if ex_stu:
            continue
        with app.app_context():
            try:
                student = Student(num=num,name=name,major=major,grade=grade,college=college,password=password)
                db.session.add(student)
                db.session.commit()

            except:
                db.session.rollback()
                db.session.commit()
                return "上传失败"

    # 导入教师信息
    tea_nrows = tea_info.nrows
    for i in range(tea_nrows):
        if i == 0:
            continue
        tea_row = tea_info.row_values(i)
        num = int(tea_row[0])
        name = tea_row[1]
        college = tea_row[2]
        password = int(tea_row[3])
        print(num, name, college, password)
        ex_tea = Teacher.query.filter_by(num=num).first()
        if ex_tea:
            continue
        with app.app_context():
            try:
                teacher = Teacher(num=num, name=name, college=college, password=password)
                db.session.add(teacher)
                db.session.commit()
                return "hello"
            except:
                db.session.rollback()
                db.session.commit()
                return "上传失败"


    return "hello"
    # return render_template('view.html',student_info=student_info,nrows=nrows)






# 管理员主页
@app.route('/term_show/<teacher_id>', methods=['GET', 'POST'])
def term_show(teacher_id):
    mouth = []
    main_list = []
    main_name = []
    master_list = []
    schedule_list = []
    count_list = []
    maseter_count = 0;
    not_master_count = 0;
    base_understand = 0;
    login_id = lg_id
    teacher_info = Teacher.query.get(int(login_id))
    schedules = teacher_info.schedule

    if request.method == 'POST':
        year = request.form.get('year')
        term = request.form.get('term')
        print("year,classes", year, term)
        if term == '1':
            mouth = ['09', '10', '11', '12', '01']
        elif term == '2':
            mouth = ['02', '03', '04', '05', '06', '07', '08']

        if (term == '2'):
            tmp_year = int(year)
            year = tmp_year + 1
            print("转换后", type(year), year)
        # Schedule.query.filter(Schedule.teacher_id == int(teacher_id)).filter(Schedule.trem == classes).all()
        schedule_all = Schedule.query.filter_by(teacher_id=int(teacher_id)).all()
        for i in schedule_all:
            tmp = str(i.trem)
            print(tmp[0:4])

            print(tmp[5:7])
            year1 = tmp[0:4]
            mouth1 = tmp[5:7]

            if (str(year) == year1):
                for j in range(len(mouth)):
                    if mouth1 == str(mouth[j]):

                        main_list.append(i.name)
                        sch = Schedule.query.get(int(i.id))
                        clas = sch.class_point
                        for c in clas:
                            print(c.id)
                            master_count1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "全掌握").count()
                            base_understand1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "基本掌握").count()
                            not_master_count1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "未掌握").count()
                            print("master_count1", master_count1)
                            print("base_understand1", base_understand1)
                            print("not_master_count1", not_master_count1)
                            maseter_count += master_count1
                            not_master_count += not_master_count1
                            base_understand += base_understand1

                            print("知识点:", c.name, "master_count:", maseter_count, "not_master_count", not_master_count,
                                  "base_understand", base_understand)
                        count_list.append(maseter_count)
                        count_list.append(base_understand)
                        count_list.append(not_master_count)
                        maseter_count = 0
                        not_master_count = 0
                        base_understand = 0

        print("count_list", count_list)
        return render_template('term_show.html', last_year_before=the_last_before_last, teacher_id=teacher_id,
                               year=year, term=term,login_id=login_id,schedule=schedules,teacher_info = teacher_info,
                               now_year=now_year, last_year=last_year, main_list=main_list, count_list=count_list)
    else:
        year = now_year
        mouth = ['09', '10', '11', '12', '01']
        schedule_all = Schedule.query.filter_by(teacher_id=int(teacher_id)).all()
        for i in schedule_all:
            tmp = str(i.trem)
            print(tmp[0:4])
            print(tmp[5:7])
            year1 = tmp[0:4]
            mouth1 = tmp[5:7]
            if (str(year) == year1):
                for j in range(len(mouth)):
                    if mouth1 == str(mouth[j]):
                        main_list.append(i.name)
                        sch = Schedule.query.get(int(i.id))
                        clas = sch.class_point
                        for c in clas:
                            print(c.id)
                            master_count1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "全掌握").count()
                            base_understand1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "基本掌握").count()
                            not_master_count1 = Proficiency.query.filter(Proficiency.class_know_id == c.id).filter(
                                Proficiency.proficiency == "未掌握").count()
                            print("master_count1", master_count1)
                            print("base_understand1", base_understand1)
                            print("not_master_count1", not_master_count1)
                            maseter_count += master_count1
                            not_master_count += not_master_count1
                            base_understand += base_understand1

                            print("知识点:", c.name, "master_count:", maseter_count, "not_master_count", not_master_count,
                                  "base_understand", base_understand)
                        count_list.append(maseter_count)
                        count_list.append(base_understand)
                        count_list.append(not_master_count)
                        maseter_count = 0
                        not_master_count = 0
                        base_understand = 0

    return render_template('term_show.html', last_year_before=the_last_before_last, teacher_id=teacher_id,
                           year=year, term=1, login_id=login_id,schedule=schedules,teacher_info = teacher_info,
                           now_year=now_year, last_year=last_year, main_list=main_list, count_list=count_list)


# 后台管理主页
@app.route('/surper_root/')
def surper_root(page):
    return render_template('view.html')



#后台教师信息查看
@app.route('/surper_root/teacher/<page>')
def surper_root_teacher(page):
    teacher_all = Teacher.query.paginate(int(page), 10)
    return render_template('surper_root_teacher.html',teacher_all=teacher_all)

#后台学生信息查看
@app.route('/surper_root/student/<page>')
def surper_root_student(page):
    stduent_all = Student.query.paginate(int(page),10)
    return render_template('surper_root_student.html', stduent_all=stduent_all)


# 设为管理员
@app.route('/surper_root/set_root/',methods=['GET','POST'])
def surper_set_root():
    teacher_id = request.form.get('se_teacher')
    teacher = Teacher.query.get(int(teacher_id))
    with app.app_context():
        try:
            teacher.is_root = 1
            db.session.commit()
        except:
            db.session.rollback
            db.session.commit()
    return "设置成功"

# 解除管理员
@app.route('/surper_root/re_root/',methods=['GET','POST'])
def surper_re_root():
    teacher_id = request.form.get('rm_teacher')
    print("rm_teacher",teacher_id)
    teacher = Teacher.query.get(int(teacher_id))
    with app.app_context():
        try:
            teacher.is_root = 0
            db.session.commit()
        except:
            db.session.rollback
            db.session.commit()
    return "设置成功"

#管理员教师查找
@app.route('/surper_root_tea/find/<page>',methods=['GET','POST'])
def surper_root_tea_find(page):
    if request.method == 'POST':
        name1 = request.form.get('input_name')
        teacher = Teacher.query.filter(Teacher.name.contains(name1)).paginate(int(page), 10)
        return render_template('surper_tea_find.html', teacher_all=teacher)

    teacher = Teacher.query.filter(Teacher.name.contains('')).paginate(int(page), 10)
    return render_template('surper_tea_find.html', teacher_all=teacher)


#管理员学生查找
@app.route('/surper_root_stu/find/<page>',methods=['GET','POST'])
def surper_root_stu_find(page):
    if request.method == 'POST':
        name1 = request.form.get('input_name')
        student = Student.query.filter(Student.name.contains(name1)).paginate(int(page),10)
        return render_template('surper_stu_find.html', stduent_all=student)
    student = Student.query.filter(Student.name.contains('')).paginate(int(page), 10)
    return render_template('surper_stu_find.html', stduent_all=student)


#查看管理人员
@app.route('/super_root_show/<page>',methods=['GET','POST'])
def super_root_show(page):
    teacher_all = Teacher.query.filter_by(is_root='1').paginate(int(page), 10)
    return render_template('root_show.html',teacher_all=teacher_all)

if __name__ == '__main__':
    app.run()
    # app.run(host='192.168.43.139', port=5000)
