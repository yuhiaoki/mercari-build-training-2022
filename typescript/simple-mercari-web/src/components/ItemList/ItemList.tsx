import React, { useEffect, useState } from "react";

interface Item {
  id: number;
  name: string;
  category: string;
  image_filename: string;
}

const server = process.env.API_URL || "http://127.0.0.1:9000";

interface Prop {
  reload?: boolean;
  onLoadCompleted?: () => void;
}

export const ItemList: React.FC<Prop> = (props) => {
  const { reload = true, onLoadCompleted } = props;
  const [items, setItems] = useState<Item[]>([]);
  console.log(items);

  const fetchItems = () => {
    fetch(server.concat("/items"), {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("GET success:", data);
        setItems(data);
      })
      .catch((error) => {
        console.error("GET error:", error);
      });
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <div>
      {items.map((item) => {
        const placeholderImage =
          "http://127.0.0.1:9000/image/" + item?.id + ".jpg";
        return (
          <div key={item.id} className="ItemList">
            {/* TODO: Task 1: Replace the placeholder image with the item image */}
            <img src={placeholderImage} />
            <p>
              <span>Name: {item.name}</span>
              <br />
              <span>Category: {item.category}</span>
            </p>
          </div>
        );
      })}
    </div>
  );
};
