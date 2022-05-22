import React, { useState } from "react";

const server = process.env.API_URL || "http://127.0.0.1:9000";
interface Prop {
  onListingCompleted?: () => void;
}

type formDataType = {
  name: string;
  category: string;
  image: string | File;
};
export const Listing: React.FC<Prop> = (props) => {
  const { onListingCompleted } = props;
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
    console.log(values);
    data.append("name", values.name);
    data.append("category", values.category);
    data.append("image", values.image);
    console.log(data);
    fetch(server.concat("/items"), {
      method: "POST",
      mode: "cors",
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("POST success:", data);
      })
      .catch((error) => {
        console.error("POST error:", error);
      });
  };
  return (
    <div className="Listing">
      <form onSubmit={onSubmit}>
        <div>
          <input
            type="text"
            name="name"
            id="name"
            placeholder="name"
            onChange={onChange}
            required
          />
          <input
            type="text"
            name="category"
            id="category"
            placeholder="category"
            onChange={onChange}
          />
          <input
            type="file"
            name="image"
            id="image"
            placeholder="image"
            onChange={onFileChange}
          />
          <button type="submit">List this item</button>
        </div>
      </form>
    </div>
  );
};
