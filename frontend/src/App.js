import React, { useEffect, useRef } from "react";
import "./App.css";
import { BrowserRouter as Router } from "react-router-dom";
import { Chart } from "react-chartjs-2";
import { ThemeProvider } from "@material-ui/styles";
import validate from "validate.js";

import { chartjs } from "./helpers";
import theme from "./theme";
import "react-perfect-scrollbar/dist/css/styles.css";
import "./assets/scss/index.scss";
import validators from "./common/validators";
import Routes from "./Routes";
import { useDispatch, useSelector } from "react-redux";
import {
  authCheckState as onTryAutoSignIn,
  changeMessageStatus,
} from "./store/actions";
import hostName from "./helpers/hostName";

Chart.helpers.extend(Chart.elements.Rectangle.prototype, {
  draw: chartjs.draw,
});

validate.validators = {
  ...validate.validators,
  ...validators,
};

function App() {
  const ws = useRef(null);
  const dispatch = useDispatch();
  const { timer } = useSelector((state) => ({
    timer: state.security.timer,
  }));

  useEffect(() => {
    // used to restore session when user refresh the page without logging out.
    dispatch(onTryAutoSignIn());
    return () => clearTimeout(timer);
  }, [dispatch]);

  useEffect(() => {
    ws.current = new WebSocket("ws://" + hostName() + "/ws/message/");
    ws.current.onopen = () => console.log("ws opened");
    ws.current.onclose = () => console.log("ws closed");

    ws.current.onmessage = (e) => {
      const message = JSON.parse(e.data);
      dispatch(changeMessageStatus(message));
    };

    return () => {
      ws.current.close();
    };
  }, [dispatch]);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes />
      </Router>
    </ThemeProvider>
  );
}

export default App;
