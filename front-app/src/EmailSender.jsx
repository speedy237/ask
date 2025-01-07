import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from "chart.js";
  
  ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const EmailSender = () => {
  const [email, setEmail] = useState("");
  const [roleIDs, setRoleIDs] = useState([]);
  const [selectedRoleID, setSelectedRoleID] = useState("");
  const [topN, setTopN] = useState(0);
  const [allCandidates, setAllCandidates] = useState([]);
  const [topCandidates, setTopCandidates] = useState([]);
  const [message, setMessage] = useState("");
  const [showChart, setShowChart] = useState(false);
  const [allExperience, setAllExperience] = useState([]);
  const [topApplications, setTopApplications] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // Fetch RoleIDs on load
  useEffect(() => {
    const fetchRoleIDs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/role");
        const uniqueRoleIDs = [
          ...new Set(response.data.message.map((role) => role.IDjob)),
        ];
        setRoleIDs(uniqueRoleIDs);
        
      } catch (error) {
        setMessage("Failed to fetch RoleIDs.");
      }
    };
    fetchRoleIDs();
  }, []);



  

  // Fetch candidates based on RoleID
  const fetchCandidates = async () => {
    if (!selectedRoleID) {
      setMessage("Please select a RoleID.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/role/candidate/", {
        role_id: selectedRoleID,
        start_date: startDate,
        end_date: endDate,
      });
      const allFetchedCandidates = response.data;
      setAllCandidates(allFetchedCandidates);

      // Set top N candidates
      const topFetchedCandidates = allFetchedCandidates.slice(0, topN);
      setTopCandidates(topFetchedCandidates);
    } catch (error) {
      setMessage("Failed to fetch candidates.");
    }
  };

 

  // Send email
  const sendEmail = async () => {
    if (!email) {
      setMessage("Please provide an email address.");
      return;
    }

    const response = await axios.get("http://localhost:8000/all");
    const allFetchedApplication = response.data;
    setTopApplications(allFetchedApplication);

    if (topApplications.length === 0) {
      setMessage("Please fetch candidates before sending the email.");
      return;
    }


    try {
      console.log(email)
      console.log("-----------------")
      console.log(topApplications.length)
      await axios.post("http://localhost:8000/send-email", {
        email:email,
        applications: topApplications,
        topN:topN,
      });
      setMessage("Email sent successfully.");
    } catch (error) {
      setMessage("Failed to send email.");
    }
  };

  // Prepare data for the bar chart

  const fetchExperience = async () => {
    if (!selectedRoleID) {
      setMessage("Please select a RoleID.");
      return;
    }
  
    try {
      const response = await axios.post("http://localhost:8000/experience/", {
        role_id: selectedRoleID,
      });
      const fetchedExperience = response.data;
      setAllExperience(fetchedExperience || []); // Par sécurité, définir un tableau vide si les données sont nulles
      setShowChart(!showChart);
      console.table(fetchedExperience);
    } catch (error) {
      setMessage("Failed to fetch Experience.");
    }
  };
  

  const chartData = {
    labels: (allExperience || []).map((experience) => experience.Experience),
    datasets: [
      {
        label: "NombreDeCandidats",
        data: (allExperience || []).map((experience) => experience.NombreDeCandidats),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };
  

  return (
    <div className="container mt-5">
      {/* Email Input */}
      <div className="mb-3">
        <label htmlFor="email" className="form-label">
          Recipient Email
        </label>
        <input
          type="email"
          className="form-control"
          id="email"
          placeholder="Enter recipient email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      {/* RoleID Selection */}
      <div className="mb-3">
        <label htmlFor="roleID" className="form-label">
          Select RoleID
        </label>
        <select
          className="form-select"
          id="roleID"
          value={selectedRoleID}
          onChange={(e) => setSelectedRoleID(e.target.value)}
        >
          <option value="">-- Select RoleID --</option>
          {roleIDs.map((IDjob) => (
            <option key={IDjob} value={IDjob}>
              {IDjob}
            </option>
          ))}
        </select>
      </div>

       {/* Start Date Input */}
       <div className="mb-3">
        <label htmlFor="startDate" className="form-label">
          Start Date
        </label>
        <input
          type="date"
          className="form-control"
          id="startDate"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>

      {/* End Date Input */}
      <div className="mb-3">
        <label htmlFor="endDate" className="form-label">
          End Date
        </label>
        <input
          type="date"
          className="form-control"
          id="endDate"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>

      {/* Top N Input */}
      <div className="mb-3">
        <label htmlFor="topN" className="form-label">
          Number of Top Candidates
        </label>
        <input
          type="number"
          className="form-control"
          id="topN"
          placeholder="Enter the number of top candidates"
          value={topN}
          onChange={(e) => setTopN(Number(e.target.value))}
        />
      </div>

      {/* Fetch Candidates Button */}
      <button className="btn btn-primary mb-3" onClick={fetchCandidates}>
        Search Candidates
      </button>

      {/* Candidates Table */}
      {topCandidates.length > 0 && (
        <div className="mt-4">
          <h3>Top {topN} Candidates List</h3>
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Name</th>
                <th>Score</th>
                <th>Experience</th>
                <th>Date</th>
             
              </tr>
            </thead>
            <tbody>
              {topCandidates.map((candidate, index) => (
                <tr key={index}>
                  <td>{candidate.applicantName}</td>
                  <td>{candidate.Score}</td>
                  <td>{candidate.Experience}</td>
                  <td>{candidate.Date}</td>
                 
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Bar Chart Button */}
      {allCandidates.length > 0 && (
        <button
          className="btn btn-info mt-3"
          onClick={() => fetchExperience()}
        >
          {showChart ? "Hide Chart" : "Show Chart"}
        </button>
      )}

      {showChart && allExperience.length > 0 ? (
           <Bar data={chartData} />
      ) : (
           <p>No data available to display the chart.</p>
      )}


      {/* Send Email Button */}
      <button className="btn btn-success mt-3" onClick={sendEmail}>
        Send Email
      </button>

      {/* Status Message */}
      {message && <div className="alert alert-info mt-3">{message}</div>}
    </div>
  );
};

export default EmailSender;
