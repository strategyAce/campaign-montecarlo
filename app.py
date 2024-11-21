import streamlit as st
import pandas as pd
from src.auth import authenticate
from src.simulation import monte_carlo_simulation
from src.visualization import plot_election_results

# Path to assets
BANNER_PATH = "StratAceBanner_Logo.png"
LOGO_PATH = "Campaign-Predictor.png"
url = "https://strategyace.win/"

def main():
    # User session for login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Login page
    if not st.session_state.logged_in:
        st.image(BANNER_PATH,width=550)
        st.subheader(" ")
        col1,col2 = st.columns(2)
        with col1:
            st.title("Predictor Tool")
            st.subheader("Run predictions that can give your campaign an edge up on the competition")
        with col2:
            st.image(LOGO_PATH,width=225)
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.query_params.update({"logged_in": True})
            else:
                st.error("Invalid username or password.")
    else:
        # App Header
        st.image(BANNER_PATH,width=550)
        st.subheader(" ")
        col1,col2 = st.columns(2)
        with col1:
            st.title("Campaign Predictor Tool")
            st.subheader("Run predictions that can give your campaign an edge up on the competition")
        with col2: 
            st.image(LOGO_PATH, width=250)  
        st.write("This is a product of Strategy Ace LLC")
        st.write("rev:v0.1...date:09/29/2024....notes:Initial StreamLit Release")
        st.divider()

        # Initialize election_results to None
        election_results = None

        # Input Collection
        st.write("Enter Fixed Simulation Variables")
        num_runs = st.slider("Enter Number of Runs", 0, 2000, 1000,step=1)
        RegDems = st.number_input("Enter Number of Registered Democrats (fixed variable)", min_value=0, value=0, step=1)
        RegReps = st.number_input("Enter Number of Registered Republicans (fixed variable)", min_value=0, value=0, step=1)
        RegNPAs = st.number_input("Enter Number of Registered NPAs/Others (fixed variable)", min_value=0, value=0, step=1)
        st.divider()
        st.write("Enter Normal Distribution Monte Carlo Variables")
        # Create two columns
        col1, col2 = st.columns(2)
        # Add content to the first column
        with col1:
            DemMean = st.number_input("Enter mean value of Dem turnout %", min_value=0.00, max_value=100.00, value=0.00, step=1.00)
            RepMean = st.number_input("Enter mean value of Republican turnout %", min_value=0.00, max_value=100.00,value=0.00, step=1.00)            
            NPAMean = st.number_input("Enter mean value of NPA/Other turnout %", min_value=0.00, max_value=100.00, value=0.00, step=1.00)
        # Add content to the second column
        with col2:
            DemStd = st.number_input("Enter standard deviation of Dem turnout %", min_value=0.00, value=1.00, step=1.00)
            RepStd = st.number_input("Enter standard deviation of Republican turnout %", min_value=0.00, value=1.00, step=1.00)
            NPAStd = st.number_input("Enter standard deviation of NPA/Other turnout %", min_value=0.00, value=1.00, step=1.00)
        st.divider()
        st.write("Enter Uniform Distribution Monte Carlo Variables")
        Demvalues = st.slider("Enter the lower and upper % values of Democrats that vote for your candidate",0,100,(25,75))
        DemLow = Demvalues[0]
        DemHigh = Demvalues[1]
        Repvalues = st.slider("Enter the lower and upper % values of Republicans that vote for your candidate",0,100,(25,75))
        RepLow = Repvalues[0]
        RepHigh = Repvalues[1]
        NPAvalues = st.slider("Enter the lower and upper % values of NPA/Others that vote for your candidate",0,100,(25,75))
        NPALow = NPAvalues[0]
        NPAHigh = NPAvalues[1]

        if st.button("Run Simulation"):
            # Perform the Monte Carlo analysis
            election_results = monte_carlo_simulation(
                num_runs, DemLow, DemHigh, RepLow, RepHigh, NPALow, NPAHigh,
                DemMean, DemStd, RepMean, RepStd, NPAMean, NPAStd, 
                RegDems, RegReps, RegNPAs
            )
            
            if election_results is not None:
                st.write("Simulation Complete")
                st.divider()
                st.subheader("Simulation Results")
                # Calculate statistics
                Winvalues = election_results[election_results['% of Votes'] > 50.0]
                Lossvalues = election_results[election_results['% of Votes'] <= 50.0]
                
                # Display average votes
                win_stats = {
                    'Win Mean Dem Votes': Winvalues['Dem Votes'].mean(),
                    'Win Mean Rep Votes': Winvalues['Rep Votes'].mean(),
                    'Win Mean NPA Votes': Winvalues['NPA Votes'].mean()
                }
                loss_stats = {
                    'Loss Mean Dem Votes': Lossvalues['Dem Votes'].mean(),
                    'Loss Mean Rep Votes': Lossvalues['Rep Votes'].mean(),
                    'Loss Mean NPA Votes': Lossvalues['NPA Votes'].mean()
                }
                
                # Display results
                col1,col2 = st.columns(2)
                with col1:
                    Pwin = len(Winvalues)/num_runs * 100
                    st.write(f'Percentage of Wins = {Pwin:.2f}%')
                    st.write(pd.DataFrame([win_stats]).T)
                with col2:
                    Ploss = len(Lossvalues)/num_runs * 100
                    st.write(f'Percentage of Loss = {Ploss:.2f}%')
                    st.write(pd.DataFrame([loss_stats]).T)
                st.write("Full Simualtion Results Data")
                st.write(election_results)
                
                # Plot results
                fig = plot_election_results(election_results)
                st.pyplot(fig)

                st.divider()
                st.image(BANNER_PATH,width=300)
                st.write(url)

if __name__ == "__main__":
    main()
