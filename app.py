import streamlit as st
import pandas as pd
import pickle
import requests

# Loading the trained ML model
filename = 'RF_placement_model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))

# Define Main function
def main():
    st.title('Campus Recruitment Prediction 🎓')

    # Center-align the layout
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container {
            max-width: 800px;
            padding-top: 50px;
            padding-right: 50px;
            padding-left: 50px;
            padding-bottom: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display form for user inputs
    st.header('Enter Candidate Details:')
    form_data = {}
    form_data['gender'] = st.selectbox('Gender', ['Male', 'Female'])
    form_data['ssc_p'] = st.number_input('SSC Percentage', min_value=0.0, max_value=100.0, step=0.1)
    form_data['ssc_b'] = st.selectbox('SSC Board', ['Central', 'Others'])
    form_data['hsc_p'] = st.number_input('HSC Percentage', min_value=0.0, max_value=100.0, step=0.1)
    form_data['hsc_b'] = st.selectbox('HSC Board', ['Central', 'Others'])
    form_data['hsc_s'] = st.selectbox('HSC Stream', ['Commerce', 'Science', 'Arts'])
    form_data['degree_p'] = st.number_input('Degree Percentage', min_value=0.0, max_value=100.0, step=0.1)
    form_data['degree_t'] = st.selectbox('Degree Type', ['Comm&Mgmt', 'Others', 'Sci&Tech'])
    form_data['workex'] = st.selectbox('Work Experience', ['No', 'Yes'])
    form_data['etest_p'] = st.number_input('E-Test Percentage', min_value=0.0, max_value=100.0, step=0.1)
    form_data['specialisation'] = st.selectbox('Specialization', ['Mkt&Fin', 'Mkt&HR'])
    form_data['mba_p'] = st.number_input('MBA Percentage', min_value=0.0, max_value=100.0, step=0.1)

    if st.button('Predict'):

        # Convert form data to DataFrame
        df = pd.DataFrame(form_data, index=[0])

        # Map categorical values to encoded values
        df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
        df['ssc_b'] = df['ssc_b'].map({'Central': 1, 'Others': 0})
        df['hsc_b'] = df['hsc_b'].map({'Central': 1, 'Others': 0})
        df['hsc_s'] = df['hsc_s'].map({'Commerce': 1, 'Science': 2, 'Arts': 0})
        df['degree_t'] = df['degree_t'].map({'Comm&Mgmt': 0, 'Others': 1, 'Sci&Tech': 2})
        df['workex'] = df['workex'].map({'No': 0, 'Yes': 1})
        df['specialisation'] = df['specialisation'].map({'Mkt&Fin': 0, 'Mkt&HR': 1})

        st.markdown('<h3 class="prediction-header">Prediction Result:</h3>', unsafe_allow_html=True)
        
        # Predict placement status using the loaded model
        predict = loaded_model.predict(df)

        if predict[0] == 1:
            st.header('The candidate is placed 🎉')
        else:
            st.header('The candidate is not placed 😞')
            
        # Display prediction result
        # st.header('Prediction Result:')
        # st.write(result)

if __name__ == '__main__':
    main()