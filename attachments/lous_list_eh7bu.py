# Elizabeth Henning eh7bu

import urllib.request

def instructors(department):

    url = "http://cs1110.cs.virginia.edu/files/louslist/" + department
    stream = urllib.request.urlopen(url)

    data = []

    for line in stream:
        column = line.decode("UTF-8").strip().split("|")
        data.append(column)

    instructor_names = []

    for column in data:
        instructor_name = column[4].strip('+1').strip('+2').strip('+3').strip('+4')
        if instructor_name not in instructor_names:
            instructor_names.append(instructor_name)

    instructor_names.sort()

    return instructor_names


def class_search(dept_name, has_seats_available = True, level = None, not_before = None, not_after = None):

    final_classes = []

    url = "http://cs1110.cs.virginia.edu/files/louslist/" + dept_name
    stream = urllib.request.urlopen(url)

    class_data = []

    for column in stream:
        column = column.decode("UTF-8").strip().split("|")
    
        seats = False
        enrolled = column[15]
        available = column[16]
        if int(enrolled) < int(available) or has_seats_available is False:
            seats = True

        lev = False
        course_level = column[1]
        if (level // 1000) == int(course_level[0]):
            lev = True

        before = False
        if not_before is None:
            before = True
        else:
            first_time = column[12]
            if int(first_time) >= int(not_before):
                before = True

        after = False
        if not_after is None:
            after = True
        else:
            last_time = column[12]
            if int(last_time) < int(not_after):
                after = True

        if seats and lev and before and after:
            final_classes.append(column)

    return final_classes
