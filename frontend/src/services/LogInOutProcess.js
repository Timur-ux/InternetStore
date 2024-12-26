import { AuthStatus, onLogOut } from "../app/reducers/authData";

export const LogInOutProcess = (authStatus) => {
  if (authStatus == AuthStatus.logged) {
    console.log("TODO: add cookies clean when log out");
    return ({dispatch, navigate}) => {
      dispatch(onLogOut());
      navigate("/");
    }
  }
  else if (authStatus == AuthStatus.notLogged) {
    return ({dispatch = null, navigate}) => navigate("/auth");
  } 

  console.log("LogInOutProcess: error: undefined authStatus: ", authStatus);
  return () => {};
}
