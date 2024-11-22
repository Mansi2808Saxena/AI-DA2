% Load the library for handling CSV files
:- use_module(library(csv)).

% Load the data from a CSV file into Prolog facts
load_csv_data :-
    csv_read_file("data.csv", Rows, [functor(student), arity(3)]),
    maplist(assert, Rows).

% Rule to check if a student is eligible for a scholarship
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_Percentage, CGPA),
    Attendance_Percentage >= 75,
    CGPA >= 9.0.

% Rule to check if a student is permitted to sit for exams
permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_Percentage, _),
    Attendance_Percentage >= 75.
% Load the HTTP library
:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).

% Start the HTTP server on port 8080
start_server :-
    http_server(http_dispatch, [port(8080)]).

% Define API endpoints
:- http_handler('/scholarship', scholarship_handler, []).
:- http_handler('/exam_permission', exam_permission_handler, []).

% Scholarship Eligibility Handler
scholarship_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    ( eligible_for_scholarship(Student_ID)
    -> reply_json_dict(_{student_id: Student_ID, eligible: true})
    ; reply_json_dict(_{student_id: Student_ID, eligible: false})
    ).

% Exam Permission Handler
exam_permission_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    ( permitted_for_exam(Student_ID)
    -> reply_json_dict(_{student_id: Student_ID, permitted: true})
    ; reply_json_dict(_{student_id: Student_ID, permitted: false})
    ).
