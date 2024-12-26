import { AuthStatus, onLogOut } from "../app/reducers/authData";
import client from "./client";

export const LogInOutProcess = async (authStatus) => {
  if (authStatus == AuthStatus.logged) {
    return async ({dispatch, navigate}) => {
      dispatch(onLogOut());
      navigate("/");
      await client.post("/logout");
    }
  }
  else if (authStatus == AuthStatus.notLogged) {
    return async ({dispatch = null, navigate}) => navigate("/auth");
  } 

  console.log("LogInOutProcess: error: undefined authStatus: ", authStatus);
  return () => {};
}
