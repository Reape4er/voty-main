from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

nominations_users = db.Table(
    "nominations_users",
    db.Column("nomination_id", db.Integer, db.ForeignKey("nominations.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
)


# На него ссылаются номинации из таблицы связи и двух таблиц оценки
class Users(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    patronymic = db.Column(db.String(80))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    # Роль: 0 - Организатор, 1 - Эксперт.
    role = db.Column(db.String(30), nullable=False)
    ratings = db.relationship("RatingEvaluations", backref="users")
    arithmetics = db.relationship("ArithmeticEvaluations", backref="users")

    @property
    def password(self):
        raise AttributeError("password is not readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        #извлекаем все значения по столбцам за исключением пароля
        user_data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password_hash'}
        return user_data

# На него ссылаются формами, номинациями, рейтинг параметрами и арифметическими параметрами
class Events(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_description = db.Column(db.String(790), nullable=False)
    event_level = db.Column(db.Integer, nullable=False)
    # Метод оценивания: 0 - Арифметический, 1 - Рейтинговый.
    evaluation_method = db.Column(db.Integer, nullable=False)
    event_questions = db.relationship("EventQuestions", backref="events", cascade="all, delete-orphan")
    nominations = db.relationship("Nominations", backref="events", cascade="all, delete-orphan")
    ratings_parameters = db.relationship("RatingMethodParams", backref="events", cascade="all, delete-orphan")
    arithmetics_parameters = db.relationship("ArithmeticalMethodParams", backref="events", cascade="all, delete-orphan")
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    


# Сюда ссылается формы анкет
class EventQuestions(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    # form_field_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    question_field = db.Column(db.String(300), nullable=False)
    question_field_note = db.Column(db.String(300))
    question_field_type = db.Column(db.String)
    required = db.Column(db.Boolean, nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    display = db.Column(db.Boolean, default=False, nullable=False)
    application_fields = db.relationship(
        "ApplicationsFields", backref="event_questions"
    )
    question_options = db.relationship("QuestionOptions", backref="event_questions", lazy='joined')


class QuestionOptions(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    field_id = db.Column(
        db.Integer, db.ForeignKey("event_questions.id"), nullable=False
    )  # <--- связь с полем
    field_option = db.Column(db.String(160))


# Сюда ссылаются анкеты, рейтинговая и арифметическая таблица подсчетов. и многие ко многим юзеры
class Nominations(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nomination_name = db.Column(db.String(255), nullable=False)
    # Добавить дополнительную информацию
    nomination_description = db.Column(db.String(790))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    nomination_status = db.Column(db.Integer, nullable=False)
    applications = db.relationship("Applications", backref="nominations", cascade="all, delete-orphan")
    arithmetic_evaluations = db.relationship(
        "ArithmeticEvaluations", backref="nominations"
    )
    rating_evaluations = db.relationship("RatingEvaluations", backref="nominations")
    nomination_results = db.relationship("NominationResults", backref="nominations")
    users = db.relationship("Users", secondary=nominations_users, backref="nominations", lazy='joined')

    def to_dict(self):
        nomination_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # Добавляем список экспертов
        #nomination_data['experts'] = [user.to_dict() for user in self.users]
        return nomination_data
    

class NominationResults(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nomination_id = db.Column(
        db.Integer, db.ForeignKey("nominations.id"), nullable=False
    )
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    result = db.Column(db.Integer, nullable=False)
    additional_score = db.Column(db.Integer)
    total_result = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    comments = db.Column(db.Text)
    def to_dict(self):
        nomination_results_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return nomination_results_data

class Applications(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    application_status = db.Column(db.Boolean, nullable=False)
    nomination_id = db.Column(
        db.Integer, db.ForeignKey("nominations.id"), nullable=False
    )
    applications_fields = db.relationship("ApplicationsFields", backref="applications", cascade="all, delete-orphan", lazy = "joined")
    arithmetic_evaluations = db.relationship(
        "ArithmeticEvaluations", backref="applications"
    )
    rating_evaluations = db.relationship("RatingEvaluations", backref="applications")
    nomination_results = db.relationship("NominationResults", backref="applications")
    def full_application_dict(application):
        result_dict = {}
        short_info = []
        for field in application.applications_fields:
            event_question_name = field.event_questions.question_field
            result_dict[event_question_name] = field.question_answer
            if field.event_questions.display:
                short_info.append(field.event_questions.question_field)
        result_dict['short_info_columns'] = short_info
        result_dict['status'] = application.application_status
        result_dict['id'] = application.id
        return result_dict

class ApplicationsFields(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("event_questions.id"), nullable=False
    )
    question_answer = db.Column(db.String(790), nullable=False)
    # event_question = db.relationship("EventQuestions", backref="applications_fields")

class ArithmeticalMethodParams(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    criteria = db.Column(db.String(250), nullable=False)
    criteria_weight = db.Column(db.Integer, nullable=False)
    arithmetic_evaluations = db.relationship(
        "ArithmeticEvaluations", backref="arithmetical_method_params"
    )
    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ArithmeticEvaluations(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nomination_id = db.Column(
        db.Integer, db.ForeignKey("nominations.id"), nullable=False
    )
    expert_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    criteria_id = db.Column(
        db.Integer, db.ForeignKey("arithmetical_method_params.id"), nullable=False
    )
    value = db.Column(db.Integer, nullable=False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RatingMethodParams(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    position_count = db.Column(db.Integer, nullable=False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RatingEvaluations(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nomination_id = db.Column(
        db.Integer, db.ForeignKey("nominations.id"), nullable=False
    )
    expert_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    position = db.Column(db.Integer, nullable=False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
