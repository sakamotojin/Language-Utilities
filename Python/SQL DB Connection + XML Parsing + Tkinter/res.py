# author : sakamoto_jin

from tkinter import *
import datetime
import pyodbc
from xml.etree import ElementTree
import os
import json

file_path = "C:\\Users\\i0001425\\Desktop\\DashBoard"
sql_index_path = "create_index_template"


class Column:

    def __init__(self, data_source, schema, table, column):
        self.data_source = data_source
        self.schema = schema
        self.table = table
        self.column = column

    def __repr__(self):
        return "Column(%s, %s ,%s , %s)" % (self.data_source, self.schema, self.table, self.column)

    def __eq__(self, other):
        if isinstance(other, Column):
            return ((self.data_source == other.data_source) and (self.schema == other.schema) and (self.table == other.table) and (self.column == other.column))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

file_path = "C:\\Users\\i0001425\\Desktop\\DashBoard"


def initialise_database():

    file = open('database_info.json')
    global database_names
    database_names = json.load(file)
    file.close()
    server = 'tcp:fr0-viaas-089\INWP2A2401,10010'
    database = database_names['cockpit']
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    global cursor
    cursor = cnxn.cursor()


def initialise_graphics():

    global root
    root = Tk()
    root.geometry("1024x720")
    root.title('Dashboard Review Process Automation')

    l1 = Label(root, text=" Dashboard ID ")
    l1.place(x=20, y=50)

    global e1
    e1 = Entry(root)
    e1.place(x=100, y=50)

    button1 = Button(text="view", command=view)
    button1.place(x=250, y=45)

    l2 = Label(root, text=" SQL File Name ")
    l2.place(x=400, y=50)

    global e2
    e2 = Entry(root)
    e2.place(x=500, y=50)

    button2 = Button(text="Generate SQL", command=generate_sql)
    button2.place(x=650, y=45)

    global listbox
    listbox = Listbox(root, width=700, height=600)
    listbox.pack()
    scroll = Scrollbar(root)
    scroll.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scroll.set)
    scroll.config(command=listbox.yview)
    listbox.place(x=5, y=80)

    root.mainloop()
    print("graphics initialised")


def parse_relation_tag(relation, connection_name):

    parent = relation.attrib['Parent']

    if parent.find('.') == -1:
        parent = "catalog." + parent

    parent_schema, parent_table = parent.split('.')

    if parent_table.endswith("View"):
        parent_table = parent_table[:-4]

    parent_table_col = relation.find("KeyColumn").attrib['Parent']

    child = relation.attrib['Nested']

    if child.find('.') == -1:
        child = "catalog." + child

    child_schema, child_table = child.split('.')

    if child_table.endswith("View"):
        child_table = child_table[:-4]

    child_table_col = relation.find("KeyColumn").attrib['Nested']

    column_set.add(Column(connection_name, parent_schema, parent_table, parent_table_col))
    column_set.add(Column(connection_name, child_schema, child_table, child_table_col))

    app_str_par = connection_name + " : [  " + parent_schema + "  :  " + parent_table + " :  " + parent_table_col + "  ] "
    app_str_nes = connection_name + " : [  " + child_schema + "   :  " + child_table + "  :  " + child_table_col + "   ] "

    return app_str_par, app_str_nes


def parse_filter_tag(filter, connection_name):

    app_str_fil = connection_name + " : [ " + filter.text + " ] "

    return app_str_fil


def parse_xml(xml_string):

    xroot = ElementTree.fromstring(xml_string)

    result = []
    global column_set
    column_set = set([])

    for datasources in xroot.findall("DataSources"):
        for sqldatasrc in datasources.findall("SqlDataSource"):
            connection_name = sqldatasrc.find("Connection").attrib['Name']
            query_type = sqldatasrc.find("Query").attrib['Type']
            print(connection_name , query_type)
            for query in sqldatasrc.findall("Query"):
                if query.attrib['Type'] == "SelectQuery":
                    for tables in query.findall("Tables"):
                        for relation in tables.findall("Relation"):

                            app_str_par, app_str_nes = parse_relation_tag(relation , connection_name)
                            result.append(app_str_nes)
                            result.append(app_str_par)

                    for filter in query.findall("Filter"):
                        app_str_fil = parse_filter_tag(filter , connection_name)
                        result.append(app_str_fil)


    print(result)

    return result


def write_string_to_file(data, path):
    file_new = open(path, 'w')
    print(data, file=file_new)
    file_new.close()


def make_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)


def view():
    print('view')
    listbox.delete(0, END)
    query = "select DashboardXML from cockpit.Dashboards where id = ?"
    global dashboard_id
    dashboard_id = 0
    try:
        dashboard_id = int(e1.get())
    except:
        dashboard_id = 0

    cursor.execute(query, dashboard_id)
    xml_string = cursor.fetchone()[0]

    make_folders(file_path + "\\" + str(dashboard_id))
    write_string_to_file(xml_string, file_path + "\\" + str(dashboard_id) + "\\dashboard.xml")

    result_set = parse_xml(xml_string)

    for val in result_set:
        listbox.insert(END, val)
        print(val)
    for col in column_set:
        print(col)


def generate_sql():

    view()

    sql_create_idx = open(sql_index_path, 'r').read()
    print(sql_create_idx)

    x = datetime.datetime.now()
    format_d = "%m/%d/%Y %I:%M %p"

    date_time = str(x.strftime(format_d))
    print(date_time)
    print('in generate sql')

    try:
        sql_file_name = str(e2.get())
        if sql_file_name.find(".sql") == -1:
            sql_file_name = "default.sql"
    except:
        sql_file_name = "default.sql"

    res_string = ""
    for col in column_set:
        temp = sql_create_idx
        temp = temp.format(DATABASE=database_names[col.data_source], SCHEMA=col.schema, TABLE=col.table, COLUMN=col.column, DATE=date_time)
        res_string += (temp + "\n\n")

    make_folders(file_path + "\\" + str(dashboard_id))
    write_string_to_file(res_string, file_path + "\\" + str(dashboard_id) + "\\" + sql_file_name)

    print(sql_file_name)



initialise_database()
initialise_graphics()

