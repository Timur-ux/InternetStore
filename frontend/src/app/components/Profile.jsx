import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { LogInOutProcess } from "../../services/LogInOutProcess";
import style from "../../style";
import { AuthStatus, selectAuthStatus } from "../reducers/authData";

const Profile = () => {
  const [display, setDisplay] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const authStatus = useSelector(selectAuthStatus);

  const items = [
    {
      title: "cart",
      action: () => navigate("/cart"),
    },
    {
      title: authStatus == AuthStatus.logged ? "Log out" : "Log in",
      action: () => LogInOutProcess(authStatus)({dispatch, navigate}),
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
