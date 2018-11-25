CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE student (
  student_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

CREATE TABLE quiz (
  quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT UNIQUE NOT NULL,
  num_of_questions INTEGER NOT NULL,
  quiz_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE student_quiz_results (
  student_id INTEGER,
  quiz_id INTEGER,
  grade INTEGER,
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);
