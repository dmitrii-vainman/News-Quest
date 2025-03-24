import axios from "axios";

export const fetchHeadlines = async () => {
  try {
    const response = await axios.get("http://localhost:8000/headlines"); // Your backend API URL
    return response.data.headlines;  // Assuming your backend returns { headlines: [...] }
  } catch (error) {
    console.error("Error fetching headlines:", error);
    return [];
  }
};
