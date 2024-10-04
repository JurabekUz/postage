# # Extract the data from the image
# grades = [79.0, 85.0, 95.0, 80.0, 92.0, 90.0, 83.0, 87, 87, 90, 86, 90]
# credits = [2 , 4, 4, 4, 2, 2, 4, 2, 4, 2, 8, 22]
#
#
# def convert_to_gpa(grade):
#     if 90 <= grade <= 100:
#         return 5.0
#     elif 70 <= grade < 90:
#         return 4.0
#     elif 60 <= grade < 70:
#         return 3.0
#     else:
#         return 2.0
#
# # Convert grades to GPA
# gpa_points = [convert_to_gpa(grade) for grade in grades]
#
# # Calculate weighted GPA
# surat = 0
# for i in range(len(grades)):
#     surat += gpa_points[i] * credits[i]
# weighted_gpa = surat / sum(credits)
#
# print("gpa points: ", gpa_points)
# print("weighted gpa: ", weighted_gpa)

def format_number(number):
    print(f"M-{number:05d}")
    return f"M-{number:05d}"

# Test the function
format_number(1), format_number(13), format_number(123)
