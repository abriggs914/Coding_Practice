class Schedule:

    def __init__(self, appointments):
        self.appointments = appointments
        self.col_labels = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self.times_of_day = self.gen_times_of_day_dict()
        self.appointments_max_hours_dict = self.gen_appointment_max_hours_dict()
        self.appointments_dict = self.gen_appointment_dict()
        self.left_margin = '\n\t\t\t'
        self.right_margin = '\t\t'
        self.schedule_string = ''
        self.max_appointment_string = self.determine_max_width()
        self.max_appointment_height = self.determine_max_heights()
        # self.schedule_df = None

    def __repr__(self):
        res = self.schedule_string
        max_width = self.max_appointment_string
        left_margin = self.left_margin
        right_margin = self.right_margin
        top_perimeter = ''.join(['_' for i in range(7 * (max_width + 2))])
        empty_col_width = '|' + ''.join([' ' for i in range(max_width)]) + '|'
        bottom_perimeter = left_margin + '|' + top_perimeter[1:len(top_perimeter) - 1] + '|' + right_margin
        top_border = '\n' + left_margin + top_perimeter + right_margin
        # print(top_border)
        # building schedule top until col labels
        res += top_border + left_margin + ''.join([empty_col_width for i in range(7)]) + right_margin
        col_names_string = self.gen_col_names_string()
        res += left_margin + col_names_string
        maximum_cell_heights = self.max_appointment_height
        empty_cell_width = ''.join('|' + ''.join(['_' for i in range(max_width)]) + '|' for x in range(7))
        for time_of_day, max_num_lines in maximum_cell_heights.items():
            tab_space = '\t'
            if len(time_of_day) < 8:
                tab_space += '\t'
            if max_num_lines > 0:
                res += '\n' + time_of_day + tab_space + ''.join([empty_col_width for i in range(7)])
                for i in range(-1, max_num_lines):
                    if -1 < i < max_num_lines - 1:
                        row_appointments = self.gen_row_appointments(time_of_day)
                        res += left_margin + row_appointments + right_margin # 'TOFILL'  # ''.join([empty_col_width for i in range(7)]) + right_margi
                    elif i > -1:
                        # bottom border of cell
                        res += left_margin + empty_cell_width + right_margin
            else:
                res += '\n' + time_of_day + tab_space + empty_cell_width
                # print('len(left_margin):\t' + str(len(self.left_margin)))

        # res += left_margin + bottom_perimeter + right_margin
        return res

    def determine_max_width(self):
        max_width = 0
        col_labels = self.col_labels
        for appointment in self.appointments:
            max_width = max(max_width, len(appointment[0] + " @ " + appointment[4]))
        max_width = max(max_width, max([len(x) for x in col_labels]))
        return max_width + 2

    def gen_col_names_string(self):
        max_width = self.max_appointment_string
        col_labels = self.col_labels
        labels = []
        for day in col_labels:
            padded_day = day
            # print('padded_day:\t' + str(padded_day))
            day_len = len(day)
            diff = (max_width - day_len) // 2
            pad_size = max_width - diff
            # print('diff:\t' + str(diff) + '\tpad_size:\t' + str(pad_size) + '\tday_len:\t' + str(day_len))
            if diff % 2 == 0:
                padded_day = padded_day.ljust(pad_size)
                padded_day = padded_day.rjust(pad_size + diff)
            else:
                padded_day = padded_day.rjust(pad_size)
                padded_day = padded_day.ljust(pad_size + diff)
            labels.append(padded_day)
        empty_col_width = ''.join('|' + ''.join(['_' for i in range(max_width)]) + '|' for x in range(7))
        col_labels = '|' + '||'.join(labels) + '|'
        col_labels += self.left_margin + empty_col_width + self.right_margin #.join(['_' for i in range(7 * (max_width + 2))])
        # print('\n\'\'\'\n' + col_labels + '\n\'\'\'\n')
        return col_labels

    def gen_appointment_max_hours_dict(self):
        appointment_times = [(app[2], app[3]) for app in self.appointments]
        times_of_day = self.times_of_day
        days_involved = self.full_day_acronym()
        for i in range(len(appointment_times)):
            start = appointment_times[i][0]
            end = appointment_times[i][1]
            app_days = days_involved[i]
            # adjust for which days of the week are actually used
            start_break = start.split(':')
            # start_hour = start_break[0] + ':00 ' + start_break[1].split(' ')[1]
            end_break = end.split(':')
            # end_hour = end_break[0] + ':00 ' + end_break[1].split(' ')[1]
            # print(start_hour)
            # print(end_hour)
            start_hour_int = int(start_break[0])
            start_hour_suffix = start_break[1].split(' ')[1]
            # print('shi:\t' + str(start_hour_int))
            start_hour_int += (0 if (start_hour_suffix == 'AM' and start_hour_int < 12) or
                                    (start_hour_suffix == 'PM' and start_hour_int == 12) else 12)
            end_hour_int = int(end_break[0]) # + (0 if end_break[1].split(' ')[1] == 'AM' else 12)
            end_hour_suffix = end_break[1].split(' ')[1]
            # print('ehi:\t' + str(end_hour_int))
            end_hour_int +=  (0 if (end_hour_suffix == 'AM' and end_hour_int < 12) or
                                   (end_hour_suffix == 'PM' and end_hour_int == 12) else 12)
            # print('start_hour_int:\t' + str(start_hour_int) + '\tend_hour_int:\t' + str(end_hour_int) + '\tapp_duration:\t' + str(app_length))
            for appointment in app_days:
                for i in range(start_hour_int, end_hour_int + 1):
                    hour_num = str(i - 12) if i > 12 else str(i)
                    curr_hour = hour_num + ':00 ' + ('AM' if i < 12 or i == 24 else 'PM')
                    # print('i:\t' + str(i) + '\tappointment  day:\t' + str(appointment) + '\tcurr_hour:\t' + str(curr_hour))
                    times_of_day[curr_hour][appointment] += 1
        for time, days in times_of_day.items():
            for day in days:
                num_lines = times_of_day[time][day]
                if num_lines > 2:
                    times_of_day[time][day] += (num_lines - 2) // 2
                if times_of_day[time][day] > 0 and times_of_day[time][day] % 2 == 1:
                    times_of_day[time][day] += 1

        # print(times_of_day)
        return times_of_day

    def gen_appointment_dict(self):
        # print('gen_appointment_dict\t' + str(self.appointments))
        times = list(self.times_of_day.keys())
        hours_apps_list = [dict(zip(times, [[] for _ in range(len(times))])) for _ in range(7)]
        appointments_dict = dict(zip(self.col_labels, hours_apps_list))
        # print('col_labels:\t' + str(self.col_labels))
        # print('times:\t' + str(times))
        days_occurring = self.full_day_acronym()# appointment[1]
        for i in range(len(self.appointments)):
            appointment = self.appointments[i]
            # print('days:\t' + '#:\t' + str(len(days_occurring)) + '\t' + str(days_occurring))
            duration_times = self.gen_duration(appointment[2], appointment[3])
            # print('duration:\t' + str(duration_times))
            for day in days_occurring[i]:
                for hour in duration_times:
                    appointments_dict[day][hour] = appointment[0] + " @ " + appointment[4]

        # print('dict:\t' + str(appointments_dict))
        # raise ValueError('NOT RETURNING YET')
        return appointments_dict

    def gen_duration(self, start, end):
        start_hour, start_min = start.split(':')
        end_hour, end_min = end.split(':')
        start_hour = int(start_hour)
        end_hour = int(end_hour)
        start_hour += 12 if ((start_min[-2:] == "PM" and start_hour != 12) or
                             (start_hour == 12 and start_min[-2:] == "AM")) else 0
        end_hour += 12 if ((end_min[-2:] == "PM" and end_hour != 12) or
                           (end_hour == 12 and end_min[-2:] == "AM")) else 0
        duration_keys = []
        for h in range(start_hour, end_hour + 1):
            suffix = "AM"
            if 11 < h < 24:
                suffix = "PM"
                if h > 12:
                    h -= 12
            if h == 24:
                h -= 12
            time = str(h) + ":00 " + suffix
            duration_keys.append(time)
        return duration_keys

    def determine_max_heights(self):
        times_of_day = self.appointments_max_hours_dict
        max_lines_per_hour = {}
        for time_of_day, weekdays in times_of_day.items():
            max_lines_per_hour[time_of_day] = 2 #max([val for key, val in weekdays.items()])
        # print("max_lines_per_hour:\t" + str(max_lines_per_hour))
        return max_lines_per_hour

    def full_day_acronym(self):
        day_acronyms = [app[1] for app in self.appointments]
        app_full_days = []
        weekdays = self.col_labels
        for app in day_acronyms:
            # print('app:\t' + str(app))
            days = app.split(' ')
            app_day = []
            for day in days:
                for weekday in weekdays:
                    adj_day = ''
                    if weekday.upper().find(day) > -1:
                        adj_day = weekday
                        break
                app_day.append(adj_day)
                # print('\tday: ' + str(day))
            app_full_days.append(app_day)
        # print('app_full_days:\t' + str(app_full_days))
        return app_full_days

    def gen_times_of_day_dict(self):
        return {'1:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '2:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '3:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '4:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '5:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '6:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '7:00 AM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '8:00 AM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '9:00 AM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '10:00 AM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '11:00 AM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '12:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '1:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '2:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '3:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '4:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '5:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '6:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '7:00 PM': {'Sunday': 2,
                                    'Monday': 2,
                                    'Tuesday': 2,
                                    'Wednesday': 2,
                                    'Thursday': 2,
                                    'Friday': 2,
                                    'Saturday': 2},
                        '8:00 PM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '9:00 PM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '10:00 PM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '11:00 PM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0},
                        '12:00 AM': {'Sunday': 0,
                                    'Monday': 0,
                                    'Tuesday': 0,
                                    'Wednesday': 0,
                                    'Thursday': 0,
                                    'Friday': 0,
                                    'Saturday': 0}}

    def gen_row_appointments(self, time_of_day):
        appointments_dict = self.appointments_dict
        days_of_week = self.col_labels
        max_width = self.max_appointment_string
        empty_col_width = '|' + ''.join([' ' for i in range(max_width)]) + '|'
        # print("APPOINTMENTS DICT\n" + str(appointments_dict))
        row = ""
        for day in days_of_week:
            # print('time_of_day\t' + str(time_of_day) + ',\tappoointments_dict[time_of_day]:\t' + str(appointments_dict[day][time_of_day]))
            if len(appointments_dict[day][time_of_day]) == 0:
                row += empty_col_width
            else:
                padded_appointment = appointments_dict[day][time_of_day]
                diff = (max_width - len(padded_appointment)) // 2
                pad_size = max_width - diff
                if diff % 2 == 0:
                    padded_appointment = padded_appointment.ljust(pad_size)
                    padded_appointment = padded_appointment.rjust(pad_size + diff)
                else:
                    padded_appointment = padded_appointment.rjust(pad_size)
                    padded_appointment = padded_appointment.ljust(pad_size + diff)
                row += "|" + padded_appointment + "|"
        # print("ROW:\n" + row)
        return row


# Testing Appointments
'''
appointments = [('CS3113', 'MON WED FRI', '8:30 AM', '9:20 AM', 'GH C118'),
                ('CS4355', 'MON WED FRI', '9:30 AM', '10:20 AM', 'HH 107'),
                ('INFO3303', 'TUE THU', '9:30 AM', '10:20 AM', 'HH 107'),
                ('Ref', 'SAT', '12:00 PM', '1:30 PM', 'FHS'),
                ('Sleep', 'SUN MON TUE WED THU FRI SAT', '1:00 AM', '7:00 AM', 'Home'),
                ('TV', 'FRI', '10:00 PM', '12:00 AM', 'Home')]
'''
'''
appointments = [('CS3113', 'MON WED FRI', '8:30 AM', '9:20 AM', 'GH C122'),
                ('CS4355', 'TUE THU', '10:00 AM', '11:20 AM', 'HH C9'),
                ('CS4355 TUT', 'TUE', '2:30 PM', '3:20 PM', 'GH D124'),
                ('CS4411', 'TUE THU', '3:30 PM', '4:50 PM', 'ITC 317'),
                ('CS4411 TUT', 'THU', '2:30 PM', '3:20 PM', 'ITC 317'),
                ('ECE2214', 'MON WED FRI', '11:30 AM', '12:20 PM', 'GH C122'),
                ('ECE2214 TUT', 'TUE', '1:30 PM', '2:20 PM', 'MH 53'),
                ('ECE2215 LAB', 'WED', '2:30 PM', '4:20 PM', 'HH 117'),
                ("CS4725", "MON WED FRI", "12:30 PM", "1:20 PM", "GH C112"),
                ("CS4725 LAB", "FRI", "2:30 PM", "4:20 PM", "ITC 415")]
'''
appointments = [("CS3113", "MON WED FRI", "8:30 AM", "9:20 AM", "GH C122"),
                ("CS4355", "TUE THU", "10:00 AM", "11:20 AM", "HH C9"),
                ("CS4355 TUT", "TUE", "2:30 PM", "3:20 PM", "GH D124"),
                ("CS4411", "TUE THU", "3:30 PM", "4:50 PM", "ITC 317"),
                ("CS4411 TUT", "THU", "2:30 PM", "3:20 PM", "ITC 317"),
                ("CS3035", "TUE THU", "8:30 AM", "9:50 AM", "HH 206"),
                ("CS4725", "MON WED FRI", "12:30 PM", "1:20 PM", "GH C112"),
                ("CS4725 LAB", "FRI", "2:30 PM", "4:20 PM", "ITC 415")]
class_schedule = Schedule(appointments)
print(class_schedule)
