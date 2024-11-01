import streamlit as st
from src.auth import authenticate
from src.simulation import monte_carlo_simulation
from src.visualization import plot_election_results

def main():
    # User session for login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Login page
    if not st.session_state.logged_in:
        st.title("Login to Access Monte Carlo Election App")
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
        st.title("Monte Carlo Election Analysis Tool")
        st.subheader("This is a product of Strategy Ace LLC")
        st.write("rev:v0.1...date:09/29/2024....notes:Initial StreamLit Release")
        st.divider()

        # Initialize election_results to None
        election_results = None

        # Input Collection
        st.write("Enter Fixed Simulation Variables")
        num_runs = st.number_input("Enter Number of Runs", min_value=0, value=0, step=1)
        RegDems = st.number_input("Enter Number of Registered Democrats (fixed variable)", min_value=0, value=0, step=1)
        RegReps = st.number_input("Enter Number of Registered Republicans (fixed variable)", min_value=0, value=0, step=1)
        RegNPAs = st.number_input("Enter Number of Registered NPAs/Others (fixed variable)", min_value=0, value=0, step=1)

        st.write("Enter Normal Distribution Monte Carlo Variables")
        DemMean = st.number_input("Enter mean value of Dem turnout %", min_value=0, value=0, step=1)
        DemStd = st.number_input("Enter standard deviation of Dem turnout %", min_value=0, value=0, step=1)
        RepMean = st.number_input("Enter mean value of Republican turnout %", min_value=0, value=0, step=1)
        RepStd = st.number_input("Enter standard deviation of Republican turnout %", min_value=0, value=0, step=1)
        NPAMean = st.number_input("Enter mean value of NPA/Other turnout %", min_value=0, value=0, step=1)
        NPAStd = st.number_input("Enter standard deviation of NPA/Other turnout %", min_value=0, value=0, step=1)

        st.write("Enter Uniform Distribution Monte Carlo Variables")
        DemLow = st.number_input("Enter the lower % value of Democrats that vote for your candidate", min_value=0, value=0, step=1)
        DemHigh = st.number_input("Enter the upper % value of Democrats that vote for your candidate", min_value=0, value=0, step=1)
        RepLow = st.number_input("Enter the lower % value of Republicans that vote for your candidate", min_value=0, value=0, step=1)
        RepHigh = st.number_input("Enter the upper % value of Republicans that vote for your candidate", min_value=0, value=0, step=1)
        NPALow = st.number_input("Enter the lower % value of NPA/Others that vote for your candidate", min_value=0, value=0, step=1)
        NPAHigh = st.number_input("Enter the upper % value of NPA/Others that vote for your candidate", min_value=0, value=0, step=1)

        if st.button("Run Simulation"):
            # Perform the Monte Carlo analysis
            election_results = monte_carlo_simulation(
                num_runs, DemLow, DemHigh, RepLow, RepHigh, NPALow, NPAHigh,
                DemMean, DemStd, RepMean, RepStd, NPAMean, NPAStd, 
                RegDems, RegReps, RegNPAs
            )
            
            if election_results is not None:
                st.write("Simulation Complete")
                st.write("Here are the results:")
                
                # Calculate statistics
                Winvalues = election_results[election_results['% of Votes'] > 50.0]
                Lossvalues = election_results[election_results['% of Votes'] <= 50.0]
                
                # Display results
                st.write('Percentage of Wins = ', len(Winvalues)/num_runs * 100)
                st.write('Percentage of Loss = ', len(Lossvalues)/num_runs * 100)
                
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
                
                st.write(pd.DataFrame([win_stats]).T)
                st.write(pd.DataFrame([loss_stats]).T)
                st.write(election_results)
                
                # Plot results
                fig = plot_election_results(election_results)
                st.pyplot(fig)

if __name__ == "__main__":
    main()
