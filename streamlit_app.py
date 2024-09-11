import streamlit as st
import snowflake.connector

# execute SF queries
def get_sf_dropdown_values(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetch_pandas_all()
        
# open snowflake connection
conn = snowflake.connector.connect(**st.secrets["snowflake"])

# populate dropdown values from SF queries - TODO insert more queries

sql = "select name from PRJ_ROLES UNION SELECT name from FR_ROLES"
FR_PR_Values = get_sf_dropdown_values(sql)

sql = "select name from users_tbl where name ilike 'SVC%'"
Svc_User_Values = get_sf_dropdown_values(sql)

sql = "select name from users_tbl where name not ilike 'SVC%'"
User_Values = get_sf_dropdown_values(sql)

# close snowflake connection
conn.close()

selected_usertype = st.radio(
        "Add functional/project role(s) to ",
        ["Service Account", "Individual User"],        
        index=None,
        key='user_radio'
    )
st.write(f'the selected user is:{addFunctionalRoleToUser}')

# create form
st.header('Snowflake User Access Request Form')
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

    # TODO - need to fix conditional logic using st.empty https://discuss.streamlit.io/t/can-i-add-to-a-selectbox-an-other-option-where-the-user-can-add-his-own-answer/28525/5

    col1, col2 = st.columns(2)

    FrPrRoleValues = col1.multiselect(
        "Choose functional/project role(s)",
        (FR_PR_Values),
        placeholder="roles you'd like to add to your current access",
        help="Choose functional roles you'd like to add to your current access"
    )

    if selected_usertype == 'svc':
        UserValues = col2.selectbox(
            "Choose a user",
            (Svc_User_Values),
            index=None,
            placeholder="user you'd like to add the additional access",
            help="Choose a user that you'd like to add the additional access"
        )
    else:
        UserValues = col2.selectbox(
        "Choose a user",
        (User_Values),
        index=None,
        placeholder="user you'd like to add the additional access",
        help="Choose a user that you'd like to add the additional access"
        )

    reasonForRequest = st.text_area(
        "Business justification",
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
