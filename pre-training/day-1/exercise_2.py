
def grade_classification(score):
    if score >= 90:
        return "Distinction"
    elif score >= 60 and score < 90:
        return "Pass"
    else:
        return "Fail"
    
# Test the function with different scores
scores = [45, 72, 91, 60, 38, 85]
for score in scores:
    print(f"Score: {score}, Classification: {grade_classification(score)}")

# Output:
# Score: 45, Classification: Fail
# Score: 72, Classification: Pass
# Score: 91, Classification: Distinction
# Score: 60, Classification: Pass
# Score: 38, Classification: Fail
# Score: 85, Classification: Pass