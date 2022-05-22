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
  add?: boolean;
  handleAdd?: (e: boolean) => void;
}

export const ItemList = ({
  reload = true,
  onLoadCompleted,
  add,
  handleAdd,
}: Prop) => {
  const [items, setItems] = useState<Item[]>([]);
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
    handleAdd?.(false);
  }, [add]);
  return (
    <div className="list-container">
      {items.map((item) => {
        const placeholderImage =
          "http://127.0.0.1:9000/image/" + item?.id + ".jpg";
        return (
          <li key={item.id} className="ItemList">
            {/* TODO: Task 1: Replace the placeholder image with the item image */}
            <div className="img">
              <img src={placeholderImage} />
            </div>
            <p>商品名: {item.name}</p>
            <p>カテゴリー: {item.category}</p>
          </li>
        );
      })}
    </div>
  );
};
