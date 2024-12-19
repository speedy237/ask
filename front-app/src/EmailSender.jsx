import React, { useState, useEffect } from "react";
import axios from "axios";

const EmailSender = () => {
  const [email, setEmail] = useState("");
  const [roleIDs, setRoleIDs] = useState([]);
  const [selectedRoleID, setSelectedRoleID] = useState("");
  const [topN, setTopN] = useState(0);
  const [candidates, setCandidates] = useState([]);
  const [message, setMessage] = useState("");

  // Fetch RoleIDs on load
  useEffect(() => {
    const fetchRoleIDs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/role");
        const uniqueRoleIDs = [
          ...new Set(response.data.message.map((role) => role.IDjob)),
        ]; // Extract unique RoleIDs
        setRoleIDs(uniqueRoleIDs);
      } catch (error) {
        setMessage("Failed to fetch RoleIDs.");
      }
    };
    fetchRoleIDs();
  }, []);

  // Fetch candidates based on RoleID and Top N
  const fetchCandidates = async () => {
    if (!selectedRoleID || topN <= 0) {
      setMessage("Please select a RoleID and enter a valid number of candidates.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/candidates", {
        role_id: selectedRoleID,
        top_n: topN,
      });
      setCandidates(response.data);
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
    if (candidates.length === 0) {
      setMessage("Please fetch candidates before sending the email.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/send-email", {
        email,
        candidates
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Failed to send email.");
    }
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
        Fetch Candidates
      </button>

      {/* Candidates Table */}
      {candidates.length > 0 && (
        <div className="mt-4">
          <h3>Candidates List</h3>
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Name</th>
                <th>Score</th>
                <th>Experience</th>
                <th>Certification</th>
                <th>Diplome</th>
                <th>Soft Skills</th>
                <th>Hard Skills</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((candidate, index) => (
                <tr key={index}>
                  <td>{candidate.applicantName}</td>
                  <td>{candidate.Score}</td>
                  <td>{candidate.Experience}</td>
                  <td>{candidate.Certification}</td>
                  <td>{candidate.Diplome}</td>
                  <td>{candidate.Soft}</td>
                  <td>{candidate.Hard}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
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
