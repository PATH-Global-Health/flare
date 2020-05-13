import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import mapResponseErrors from "../../helpers/mapResponseErrors";
import { fetchLanguagesLookup } from "./languageActions";

export const fetchSubscribersSuccess = (subscribers, count) => {
  return {
    type: actionTypes.FETCH_SUBSCRIBERS_SUCCESS,
    data: subscribers,
    count: count,
  };
};

export const fetchSubscribersFail = (error) => {
  return {
    type: actionTypes.FETCH_SUBSCRIBERS_FAIL,
    error: error,
  };
};

export const fetchSubscribersStart = () => {
  return {
    type: actionTypes.FETCH_SUBSCRIBERS_START,
  };
};

export const fetchSubscribers = (limit, offset, searchTerm) => {
  return (dispatch) => {
    dispatch(fetchSubscribersStart());

    axios
      .get(`/subscribers/?limit=${limit}&offset=${offset}&search=${searchTerm}`)
      .then((res) => {
        const subscribers = [];
        const count = res.data.count;

        dispatch(fetchLanguagesLookup());

        res.data.results.forEach((subs, index) => {
          // format phone number before pushing it to subscribers array
          subs.phone_number = subs.phone_number.replace(
            /([+]{1}\d{3})(\d{3})(\d{6})/,
            "$1-$2-$3"
          );
          subscribers.push({ ...subs });
        });

        dispatch(fetchSubscribersSuccess(subscribers, count));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSubscribersFail(err.message));
        } else {
          dispatch(fetchSubscribersFail(err.response.data.message));
        }
      });
  };
};

export const saveDelSubscriberSuccess = () => {
  return {
    type: actionTypes.SAVE_SUBSCRIBER_SUCCESS,
  };
};

export const resetSaveSubscriberSuccess = () => {
  return {
    type: actionTypes.RESET_SAVE_SUBSCRIBER_SUCCESS,
  };
};

export const updateSubscriberFail = (error) => {
  return {
    type: actionTypes.UPDATE_SUBSCRIBER_FAIL,
    error: error,
  };
};

export const addSubscriber = (subs, history, errorCallback) => {
  return (dispatch) => {
    //remove - from phone number
    const subsCopy = { ...subs };
    subsCopy.phone_number = subsCopy.phone_number.replace(/-/g, "");

    axios
      .post("/subscribers/", subsCopy)
      .then((res) => {
        dispatch(saveDelSubscriberSuccess());
        history.push("/subscriber");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateSubscriberFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const fetchSubscriberSuccess = (subscriber) => {
  return {
    type: actionTypes.FETCH_SUBSCRIBER_SUCCESS,
    subscriber: subscriber,
  };
};

export const fetchSubscriberStart = () => {
  return {
    type: actionTypes.FETCH_SUBSCRIBER_START,
  };
};

export const fetchSubscriber = (subsId, history) => {
  return (dispatch) => {
    dispatch(fetchSubscriberStart());

    axios
      .get(`/subscribers/${subsId}`)
      .then((res) => {
        const subscriber = {
          phone_number: res.data.phone_number.replace(
            /([+]{1}\d{3})(\d{3})(\d{6})/,
            "$1-$2-$3"
          ),
          language: res.data.language,
        };

        dispatch(fetchSubscriberSuccess(subscriber));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSubscribersFail(err.message));
        } else {
          dispatch(fetchSubscribersFail(err.response.data.message));
        }
        history.push("/subscriber/");
      });
  };
};

export const editSubscriber = (subs, subsId, history, errorCallback) => {
  return (dispatch) => {
    //remove - from phone number
    const subsCopy = { ...subs };
    subsCopy.phone_number = subsCopy.phone_number.replace(/-/g, "");

    axios
      .put(`/subscribers/${subsId}/`, subsCopy)
      .then((res) => {
        dispatch(saveDelSubscriberSuccess());
        history.push("/subscriber");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateSubscriberFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const removeSubscriberFromList = (subsId) => {
  return {
    type: actionTypes.REMOVE_SUBSCRIBER,
    subsId: subsId,
  };
};

export const deleteSubscriber = (subsId, history) => {
  return (dispatch) => {
    axios
      .delete(`/subscribers/${subsId}/`)
      .then((res) => {
        dispatch(saveDelSubscriberSuccess());
        dispatch(removeSubscriberFromList(subsId));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSubscribersFail(err.message));
        } else {
          dispatch(fetchSubscribersFail(err.response.data.message));
        }
      });
  };
};
