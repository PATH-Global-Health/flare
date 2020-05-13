import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  count: 0,
  loadingSubscribers: false,
  saveSuccess: false,
  error: null,
  subscriber: null,
  loadingSubscriber: false,
};

const fetchSubscribersStart = (state) => {
  return {
    ...state,
    error: null,
    loadingSubscribers: true,
  };
};

const fetchSubscribersSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loadingSubscribers: false,
    error: null,
    count: action.count,
  };
};

const fetchSubscribersFail = (state, action) => {
  return {
    ...state,
    loadingSubscribers: false,
    error: action.error,
  };
};

const saveSubscriberSuccess = (state) => {
  return {
    ...state,
    saveSuccess: true,
  };
};

const resetSaveSubscriberSuccess = (state, action) => {
  return {
    ...state,
    saveSuccess: false,
  };
};

const fetchSubscriberStart = (state) => {
  return {
    ...state,
    error: null,
    loadingSubscriber: true,
  };
};

const fetchSubscriberSuccess = (state, action) => {
  return {
    ...state,
    subscriber: action.subscriber,
    loadingSubscriber: false,
  };
};

const removeSubscriberFromList = (state, action) => {
  return {
    ...state,
    data: state.data.filter((el) => el.id !== action.subsId),
  };
};

const updateSubscriberFail = (state, action) => {
  return {
    ...state,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_SUBSCRIBERS_START:
      return fetchSubscribersStart(state);
    case actionTypes.FETCH_SUBSCRIBERS_SUCCESS:
      return fetchSubscribersSuccess(state, action);
    case actionTypes.FETCH_SUBSCRIBERS_FAIL:
      return fetchSubscribersFail(state, action);
    case actionTypes.SAVE_SUBSCRIBER_SUCCESS:
      return saveSubscriberSuccess(state);
    case actionTypes.RESET_SAVE_SUBSCRIBER_SUCCESS:
      return resetSaveSubscriberSuccess(state);
    case actionTypes.FETCH_SUBSCRIBER_START:
      return fetchSubscriberStart(state);
    case actionTypes.FETCH_SUBSCRIBER_SUCCESS:
      return fetchSubscriberSuccess(state, action);
    case actionTypes.REMOVE_SUBSCRIBER:
      return removeSubscriberFromList(state, action);
    case actionTypes.UPDATE_SUBSCRIBER_FAIL:
      return updateSubscriberFail(state, action);
    default:
      return state;
  }
};

export default reducer;
