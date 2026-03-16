def calculate_average(numbers):
    if not numbers:
        return 0
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return average

def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
    
def class_topper(students):
    if not students:
        return None
    topper = max(students, key=lambda student: student['score'])
    return topper['name']

students = [
    {'name': 'Alice', 'score': [85, 90, 78], 'subject': 'Math'},
    {'name': 'Bob', 'score': [92, 88, 95], 'subject': 'Science'},
    {'name': 'Charlie', 'score': [78, 82, 75], 'subject': 'English'}
]

report = []
class_topper_name = class_topper(students)

for student in students:
    avg_score = calculate_average(student['score'])
    grade = get_grade(avg_score)
    if (student['name'] == class_topper_name):
        grade += " (Class Topper)"
    report.append({
    "avg_score": avg_score,
    "message": f"{student['name']} has an average score of {avg_score:.2f} and receives a grade of {grade}."
    })

for entry in sorted(report, key=lambda x: x["avg_score"], reverse=True):
    for avg_score, message in entry.items():
        if "Class Topper" in message:
            message = f"**{message}**"
        print(message)