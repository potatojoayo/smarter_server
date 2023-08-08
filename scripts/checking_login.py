import csv
from gym_student.models import Student


def run():
    students = Student.objects.filter(class_master__gym__name="목포 더행복한태권도",
                                      parent__user__fcm_tokens__len=0,
                                      is_deleted=False)
    parent_list = []
    for student in students:
        parent_list.append(student.parent)

    parent_list = list(set(parent_list))

    csv_file_path = 'files/로그인 안된 학부모 목록3.csv'
    field_names = ['학부모이름', '전화번호', '아이디']
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the parent data rows
        for parent in parent_list:
            writer.writerow({
                '학부모이름': parent.user.name,
                '전화번호': parent.user.phone,
                '아이디': parent.user.identification,
            })

