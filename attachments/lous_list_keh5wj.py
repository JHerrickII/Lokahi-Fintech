#Kelsey Hannifin (keh5wj)
import urllib.request



def instructors(department):

    class_data = []
    lou_list = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/louslist/' + department)
    for line in lou_list:
        line = line.decode('utf-8')
        cells = line.strip().split('|')
        class_data.append(cells)

    instructor_list = []
    for line in class_data:
        prof_name = line[4].strip('+1').strip('+2').strip('+3').strip('+4')
        if prof_name not in instructor_list:
            instructor_list.append(prof_name)
        instructor_list.sort()
    return instructor_list





def class_search(dept_name, has_seats_available=True, level=None, not_before=None, not_after=None):
     lou_list = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/louslist/' + dept_name)
     class_data = []
     all_classes = [] # FINAL CLASSES RETURNED WITH ALL PARAMETERS FILLED
     for line in lou_list:
         line = line.decode('utf-8')
         cells = line.strip().split('|')
         class_data.append(cells)

     for line in class_data:
         seats_available = False
         enrolled = line[15]
         available = line[16]
         if int(enrolled) < int(available) or has_seats_available is False:
             seats_available = True

         class_level = False
         course_level = line[1]
         if (level // 1000) == int(course_level[0]):
             class_level = True

         time_before = False
         if not_before is None:
             time_before = True
         else:
             start_time = line[12]
             if int(start_time) >= int(not_before):
                 time_before = True

         time_after = False
         if not_after is None:
             time_after = True
         else:
             start_time_two = line[12]
             if int(start_time_two) < int(not_after):
                 time_after = True

         if seats_available is True and class_level is True and time_before is True and time_after is True:
             all_classes.append(line)
     return all_classes




