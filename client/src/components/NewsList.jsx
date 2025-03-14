import { useEffect, useState } from "react";
import { fetchNews } from "../api/fetchNews";

function NewsList() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetchNews().then(setNews);
  }, []);

  return (
    <div>
      <h2>Latest News</h2>
      <ul>
        {news.hits?.map((article) => (
          <li key={article.objectID}>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              {article.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default NewsList;
