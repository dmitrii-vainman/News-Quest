import axios from "axios";

export async function fetchNews() {
  try {
    const response = await axios.get("http://127.0.0.1:8000/news/");
    return response.data;
  } catch (error) {
    console.error("Error fetching news:", error);
    return [];
  }
}
