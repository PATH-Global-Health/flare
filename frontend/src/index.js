import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";

import { Provider } from "react-redux";
import { createStore, applyMiddleware, compose, combineReducers } from "redux";
import thunk from "redux-thunk";
import securityReducer from "./store/reducers/securityReducer";
import languageReducer from "./store/reducers/languageReducer";
import subscriberReducer from "./store/reducers/subscriberReducer";
import messageReducer from "./store/reducers/messageReducer";
import channelReducer from "./store/reducers/channelReducer";
import surveyReducer from "./store/reducers/surveyReducer";
import resultReducer from "./store/reducers/resultReducer";

const composeEnhancers =
  (process.env.NODE_ENV === "development"
    ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
    : null) || compose;

const rootReducer = combineReducers({
  security: securityReducer,
  language: languageReducer,
  subscriber: subscriberReducer,
  message: messageReducer,
  channel: channelReducer,
  survey: surveyReducer,
  result: resultReducer,
});

const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(thunk))
);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
