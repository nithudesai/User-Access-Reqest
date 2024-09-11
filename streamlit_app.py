import streamlit as st
import snowflake.connector

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over [docs.streamlit.io](https://docs.streamlit.io/)."
)

# execute SF queries
def get_sf_dropdown_values(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetch_pandas_all()
        
# open snowflake connection
conn = snowflake.connector.connect(**st.secrets["snowflake"])

# populate dropdown values from SF queries - TODO insert more queries
sql = "select name from FR_ROLES"
Func_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES"
Prj_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES UNION SELECT name from FR_ROLES"
FR_PR_Values = get_sf_dropdown_values(sql)

sql = "select name from SVC_ROLES"
Svc_Roles_Values = get_sf_dropdown_values(sql)

# close snowflake connection
conn.close()

# create form
st.header('Snowflake Role Request Form')
with st.form("form1", clear_on_submit = True):
    #requestType = st.empty()
    snowflakeAccount = st.selectbox(
        "Snowflake Account",
        ("US", "EU"),
        index=0,
        placeholder="Select US or EU",
    )

    environments = st.multiselect(
        "Environment(s)",
        ["DEV", "TST", "PRD"],
    )
    st.write(f'the selected value is :{environments}')
    requestType = st.selectbox(
        "Type of Request",
        ("Grant Functional Role(s) to a Project Role", "Grant Functional/Project Role(s) to a Service Role", "Revoke"),
        index=None,
    )
    st.write(f'the selected value 1 is :{requestType}')
    if requestType:
        st.write(f'the selected value 2 is :{requestType}')
    # TODO - need to fix conditional logic using st.empty https://discuss.streamlit.io/t/can-i-add-to-a-selectbox-an-other-option-where-the-user-can-add-his-own-answer/28525/5
    addFunctionalRoleToProjectRole = st.radio(
        "Add functional role(s) to a project role?",
        ["Yes", "No"],        
        index=None,
    )

    addFunctionalRoleToServiceAccountRole = st.radio(
        "Add functional/project role(s) to a service account role?",
        ["Yes", "No"],
        index=None,
    )

    placeholder = st.empty()

    if requestType == "Revoke":
        st.write(f'the selected value 3 is :{requestType}')
    #if requestType == "Revoke":
    #    removeFunctionalRoleFromProjectRole = st.radio(
    #    "Remove functional role(s) from project role(s)?",
    #    ["Yes", "No"],
    #    index=None,
    #    )

    #   removeFunctionalRoleFromServiceAccountRole = st.radio(
    #    "Remove functional role(s) from service account role(s)?",
    #    ["Yes", "No"],
    #    index=None,
    #    )

    col1, col2 = st.columns(2)

    FrRoleValues = col1.multiselect(
        "Choose functional role(s)",
        (Func_Roles_Values),
        placeholder="roles you'd like to add to target project role",
        help="Choose functional roles you'd like to add to your project role"
    )

    PrjRoleValues = col2.selectbox(
        "Choose a target Project role",
        (Prj_Roles_Values),
        index=None,
        placeholder="role you'd like to add the additional access",
        help="Choose a target project tole that you'd like to add the additional access"
    )

    col3, col4 = st.columns(2)
    FrPrRoleValues = col3.multiselect(
        "Choose functional/project role(s)",
        (FR_PR_Values),
    )

    SvcRoleValues = col4.selectbox(
        "Choose a target Service Acct role",
        (Svc_Roles_Values),
        index=None,
    )

    reasonForRequest = st.text_area(
        "Reason for Request",
        "Please enter a brief description here",
    )

    # TODO - add validation to enforce mandatory fields
    submit = st.form_submit_button("Submit")

    # print form responses
    if submit:
        st.header('Form Responses')
        st.write("Snowflake Account: ", snowflakeAccount)
        st.write("Environment(s): ", environments)
        st.write("Type of Request: ", requestType)
        # TODO add role options 
    
        st.write("Reason for Request: ", reasonForRequest)
