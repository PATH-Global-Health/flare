import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import mapResponseErrors from "../../helpers/mapResponseErrors";
import { logout } from "./securityActions";
import { fetchLanguagesLookup } from "./languageActions";
import { fetchChannelsLookup } from "./channelActions";

export const fetchMessagesSuccess = (messages, count) => {
  return {
    type: actionTypes.FETCH_MESSAGES_SUCCESS,
    data: messages,
    count: count,
  };
};

export const fetchMessagesFail = (error) => {
  return {
    type: actionTypes.FETCH_MESSAGES_FAIL,
    error: error,
  };
};

export const fetchMessagesStart = () => {
  return {
    type: actionTypes.FETCH_MESSAGES_START,
  };
};

export const fetchMessages = (limit, offset, searchTerm) => {
  return (dispatch) => {
    dispatch(fetchMessagesStart());

    axios
      .get(`/messages/?limit=${limit}&offset=${offset}&search=${searchTerm}`)
      .then((res) => {
        dispatch(fetchLanguagesLookup());
        dispatch(fetchChannelsLookup());

        const messages = [];
        const count = res.data.count;

        res.data.results.forEach((msg, index) => messages.push({ ...msg }));

        dispatch(fetchMessagesSuccess(messages, count));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchMessagesFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchMessagesFail(err.response.data.message));
          }
        }
      });
  };
};

export const saveDelMessageSuccess = () => {
  return {
    type: actionTypes.SAVE_MESSAGE_SUCCESS,
  };
};

export const resetSaveMessageSuccess = () => {
  return {
    type: actionTypes.RESET_SAVE_MESSAGE_SUCCESS,
  };
};

export const updateMessageFail = (error) => {
  return {
    type: actionTypes.UPDATE_MESSAGE_FAIL,
    error: error,
  };
};

export const addMessage = (msg, history, errorCallback) => {
  return (dispatch) => {
    const channels = [];
    const languages = [];

    // Restructure array of object into array of values
    msg.channels.forEach((c, index) => channels.push(c.value));
    msg.languages.forEach((lang, index) => languages.push(lang.value));
    const message = { ...msg, channels, languages };

    axios
      .post("/messages/", message)
      .then((res) => {
        dispatch(saveDelMessageSuccess());
        history.push("/message");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateMessageFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const changeMessageStatus = (data) => {
  return {
    type: actionTypes.CHANGE_MESSAGE_STATUS,
    data: data,
  };
};
