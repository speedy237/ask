import React from 'react';
import NavComponent from './navComponent';

function Job() {
  return (
    <>
      <NavComponent />
      <div style={{ padding: '20px' }}>
        <h1>Available Jobs</h1>
        <ul>
          <li>
            <h2>Frontend Developer</h2>
            <p>Location: Paris, France</p>
            <p>Experience: 2-4 years</p>
            <p>
              Description: We are looking for a passionate Frontend Developer to join our team.
            </p>
          </li>
          <li>
            <h2>Backend Developer</h2>
            <p>Location: Lyon, France</p>
            <p>Experience: 3-5 years</p>
            <p>
              Description: Seeking a skilled Backend Developer to work on scalable applications.
            </p>
          </li>
          <li>
            <h2>Project Manager</h2>
            <p>Location: Remote</p>
            <p>Experience: 5+ years</p>
            <p>
              Description: Join our team to manage projects and ensure timely delivery.
            </p>
          </li>
        </ul>
      </div>
    </>
  );
}

export default Job;
