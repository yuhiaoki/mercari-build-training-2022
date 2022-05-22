import React, { useState } from "react";

const server = process.env.API_URL || "http://127.0.0.1:9000";
interface Prop {
  onListingCompleted?: () => void;
  open?: boolean;
  updateOpen?: () => void;
  handleAdd?: (e: boolean) => void;
}

type formDataType = {
  name: string;
  category: string;
  image: string | File;
};

export function Listing({
  onListingCompleted,
  open,
  updateOpen,
  handleAdd,
}: Prop) {
  const initialState = {
    name: "",
    category: "",
    image: "",
  };
  const [values, setValues] = useState<formDataType>(initialState);
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({ ...values, [event.target.name]: event.target.value });
  };
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values,
      [event.target.name]: event.target.files![0],
    });
  };
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData();
    data.append("name", values.name);
    data.append("category", values.category);
    data.append("image", values.image);
    fetch(server.concat("/items"), {
      method: "POST",
      mode: "cors",
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("POST success:", data);
        handleAdd?.(true);
      })
      .catch((error) => {
        console.error("POST error:", error);
      });
  };
  return (
    <div className={"Listing " + open}>
      <button onClick={updateOpen} className="btn">
        <b>Close</b>
      </button>
      <form onSubmit={onSubmit}>
        <ul className="input-container">
          <li className="input-list">
            <label>商品名</label>
            <input
              type="text"
              name="name"
              id="name"
              placeholder="name"
              onChange={onChange}
              required
            />
          </li>
          <li className="input-list">
            <label>カテゴリー</label>
            <input
              type="text"
              name="category"
              id="category"
              placeholder="category"
              onChange={onChange}
            />
          </li>
          <li className="input-list">
            <label>商品イメージ</label>
            <input
              type="file"
              name="image"
              id="image"
              placeholder="image"
              onChange={onFileChange}
            />
          </li>
        </ul>
        <button type="submit">List this item</button>
      </form>
    </div>
  );
}
