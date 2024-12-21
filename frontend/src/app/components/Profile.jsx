import React, { act, useState } from "react";
import { useNavigate } from "react-router-dom";
import style from "../../style";

const Profile = () => {
  const [display, setDisplay] = useState(false);
  const navigate = useNavigate();

  const items = [
    {
      title: "cart",
      action: () => navigate("/cart"),
    },
    {
      title: "Log out",
      action: () => console.log("Process log out"),
    }
  ];

  const itemsElements = items.map((item) => <button style={style.profileButton} onClick={item.action}>{item.title}</button>)

  return (
<div style={{...style.profileLine}}>
  {display && itemsElements}   
  <button style={{...style.profileButton}} onClick={() => setDisplay(!display)}>Profile</button>
</div>
  );
}

export default Profile;
