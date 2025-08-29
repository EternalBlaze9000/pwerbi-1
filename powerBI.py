import streamlit as st
import pandas as pd

#------------------------------------------------------------------
#3 display table function
def create_table_from_arrays(numeric_headers, non_numeric_headers):
    st.write("perform Explicit search:")
    searchedText = "" # RAW DECLARATION, value not assigned yet
    filtered_rows = pd.DataFrame()  # Initialize filtered_rows

    # 3.1 combine the nuneric and non-numberic contents into a single array
    all_headers = ["Select from dropdown"]+numeric_headers + non_numeric_headers
    col1, col2, col3 = st.columns(3)
        #here, col1 and col2 two are the placeholders. Anything you write inside with col1: will appear in the first column. And so on

    with col1:
        chooseHeader = st.selectbox("Search from:",all_headers, key="headers")
    with col2:
        operatorArray=["equal to","greater than","less than","greater than equal to","less than equal to"]
        chooseOperator = st.selectbox("Search from:", operatorArray, key="chooseOperator")
    with col3:
        if chooseHeader !="Select from dropdown":
            searchedText=st.text_input(f"enter the data from {chooseHeader}")

    # 3.2 performs search and error handling
    if chooseHeader != "Select from dropdown":  
            # If user typed something, filter the DataFrame
        if pd.api.types.is_numeric_dtype(df[chooseHeader]):
            # filtered_rows = df[df[chooseHeader].astype(str) == searchedText]
            try:
                column_data = pd.to_numeric(df[chooseHeader], errors="coerce")
                searched_value = pd.to_numeric(searchedText, errors="coerce")
            except:
                column_data = df[chooseHeader]
                searched_value = searchedText

            if chooseOperator == "equal to":
                filtered_rows = df[column_data == searched_value]
            elif chooseOperator == "greater than":
                filtered_rows = df[column_data > searched_value]
            elif chooseOperator == "less than":
                filtered_rows = df[column_data < searched_value]
            elif chooseOperator == "greater than equal to":
                filtered_rows = df[column_data >= searched_value]
            elif chooseOperator == "less than equal to":
                filtered_rows = df[column_data <= searched_value]
            else:
                filtered_rows = pd.DataFrame()  # empty if no valid operator

        else:
            # Text search
            filtered_rows = df[df[chooseHeader].astype(str).str.contains(searchedText, case=False, na=False)]
    else:
        st.dataframe(df) # if no column is selected, show the full table
    
        # Show results
    if not filtered_rows.empty:
        st.write("### Matching Rows:")
        st.dataframe(filtered_rows)
    else:
        st.warning("No match found!")

#------------------------------------------------------------------
#4 display graph function
def displayGraph():
    colx= st.selectbox("Select X axis", df.columns)
    coly= st.selectbox("Select Y axis", df.columns)

    if colx==coly:
        pie_data = df[colx].value_counts()
        st.write(f"Pie chart for **{colx}**")
    
        # Create a matplotlib figure
        fig, ax = plt.subplots()
        pie_data.plot.pie(autopct="%1.1f%%", ax=ax)
    
        # Pass the figure to Streamlit
        st.pyplot(fig)
    else:
        st.write(f"Bar chart for **{colx}** and **{coly}**")
        st.bar_chart(data=df, x=colx, y=coly)

    
#------------------------------------------------------------------
#1 upload a file
uploaded_file = st.file_uploader("Click to upload a file", type=["csv","xls","xlsx"])


if uploaded_file is not None:
    st.success(f"File `{uploaded_file.name}` uploaded successfully!")
    #1.1 read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        #df variable stores the data of the file 
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    #-----------------------------------------------------------    
    #2 extract the headers as numeric and non numreic
        #2.1 separate the content bases on numeric and non-numeric datatype
    numeric_headers = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    non_numeric_headers = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]

        #2.2 call a function to create tables and pass the numeric and non numberic datas in it
    create_table_from_arrays(numeric_headers, non_numeric_headers)
    if st.checkbox("display Graphs"):
        displayGraph()



