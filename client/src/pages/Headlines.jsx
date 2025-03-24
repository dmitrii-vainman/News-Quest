import React, { useEffect, useState } from "react";
import { fetchHeadlines } from "../api/fetchNews"; // Import the function

const Headlines = () => {
  const [headlines, setHeadlines] = useState([]);

  useEffect(() => {
    const getHeadlines = async () => {
      const data = await fetchHeadlines();
      setHeadlines(data);
    };
    
    getHeadlines(); // Fetch headlines when the component mounts
  }, []);

  return (
    <div>
      <h1>Headlines</h1>
      <ul>
        {headlines.map((headline, index) => (
          <li key={index}>{headline}</li>
        ))}
      </ul>
    </div>
  );
};

export default Headlines;
