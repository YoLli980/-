from exts import db
from datetime import datetime
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer,primary_key=True,unique=True)
    num = db.Column(db.Integer,nullable=False,unique=True)

    name = db.Column(db.String(4),nullable=False)
    college = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    schedule=db.relationship('Schedule', backref=db.backref('teahcers',cascade='all, delete'))
    is_root = db.Column(db.Boolean ,default=False ,nullable=True)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    num = db.Column(db.Integer,nullable=False,unique=True)
    name = db.Column(db.String(4), nullable=False)
    major= db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20),nullable=False)

    college = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    # class_point = db.relationship('Class_known', backref=db.backref('students'))
    proficiency = db.relationship('Proficiency', backref=db.backref('students',cascade='all, delete'))
    curricula= db.relationship('Curricula', backref=db.backref('students',cascade='all, delete'))
    tmp_curricula= db.relationship('Tmp_Curricula', backref=db.backref('students',cascade='all, delete'))




# 知识点
class Class_known(db.Model):
    __tablename__ = 'class_know'
    id = db.Column(db.Integer, primary_key=True, unique=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id', ondelete='CASCADE'))
    proficiency = db.relationship('Proficiency', backref=db.backref('class_kown',cascade='all, delete' ))
    # student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
# 课程表
class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    major = db.Column(db.String(30), nullable=False)
    classes =db.Column(db.String(30), nullable=False)
    college = db.Column(db.String(30), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'))
    grade = db.Column(db.String(30), nullable=False)
    random_code=db.Column(db.String(30), nullable=False)
    trem = db.Column(db.Date, index=True, default=datetime.utcnow())
    class_point=db.relationship('Class_known', backref=db.backref('schedules',cascade='all, delete'))
    curricula=db.relationship('Curricula', backref=db.backref('schedules',cascade='all, delete' ))
    tmp_curricula=db.relationship('Tmp_Curricula', backref=db.backref('schedules',cascade='all, delete'))

    # 熟练程度表




class Proficiency(db.Model):
    __tablename__ = 'proficiency'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False ,autoincrement=True)
    # 掌握情况
    proficiency = db.Column(db.String(50), nullable=True)
    # 评价
    estimate = db.Column(db.String(50), nullable=True)
    class_know_id = db.Column(db.Integer, db.ForeignKey('class_know.id', ondelete='CASCADE'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'))



class Curricula(db.Model):
    __tablename__ = 'curricula_variable'
    id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id', ondelete='CASCADE'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'))



class Tmp_Curricula(db.Model):
    __tablename__ = 'tmp_curricula'
    id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id', ondelete='CASCADE'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'))

# 超级管理员
class Surper_root(db.Model):
    __tablename__  ='root'
    id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    num =db.Column(db.Integer,nullable=False)
    name =db.Column(db.String(4),nullable=False)
    password =db.Column(db.String(25),nullable=False)

# class Root(db.Model):
#     __tablename__ = 'root'

