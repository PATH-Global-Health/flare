import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  count: 0,
  loadingMessages: false,
  saveSuccess: false,
  error: null,
  message: null,
  loadingMessage: false,
};

const fetchMessagesStart = (state) => {
  return {
    ...state,
    error: null,
    loadingMessages: true,
  };
};

const fetchMessagesSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loadingMessages: false,
    error: null,
    count: action.count,
  };
};

const fetchMessagesFail = (state, action) => {
  return {
    ...state,
    loadingMessages: false,
    error: action.error,
  };
};

const saveMessageSuccess = (state) => {
  return {
    ...state,
    saveSuccess: true,
  };
};

const resetSaveMessageSuccess = (state, action) => {
  return {
    ...state,
    saveSuccess: false,
  };
};

const fetchMessageStart = (state) => {
  return {
    ...state,
    error: null,
    loadingMessage: true,
  };
};

const fetchMessageSuccess = (state, action) => {
  return {
    ...state,
    message: action.message,
    loadingMessage: false,
  };
};

const removeMessageFromList = (state, action) => {
  return {
    ...state,
    data: state.data.filter((el) => el.id !== action.msgId),
  };
};

const updateMessageFail = (state, action) => {
  return {
    ...state,
    error: action.error,
  };
};

const changeMessageStatus = (state, action) => {
  return {
    ...state,
    data: state.data.map((obj) => {
      if (obj.id === action.data.content.messageId) {
        obj.status = action.data.content.status;
      }
      return obj;
    }),
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_MESSAGES_START:
      return fetchMessagesStart(state);
    case actionTypes.FETCH_MESSAGES_SUCCESS:
      return fetchMessagesSuccess(state, action);
    case actionTypes.FETCH_MESSAGES_FAIL:
      return fetchMessagesFail(state, action);
    case actionTypes.SAVE_MESSAGE_SUCCESS:
      return saveMessageSuccess(state);
    case actionTypes.RESET_SAVE_MESSAGE_SUCCESS:
      return resetSaveMessageSuccess(state);
    case actionTypes.FETCH_MESSAGE_START:
      return fetchMessageStart(state);
    case actionTypes.FETCH_MESSAGE_SUCCESS:
      return fetchMessageSuccess(state, action);
    case actionTypes.REMOVE_MESSAGE:
      return removeMessageFromList(state, action);
    case actionTypes.UPDATE_MESSAGE_FAIL:
      return updateMessageFail(state, action);
    case actionTypes.CHANGE_MESSAGE_STATUS:
      return changeMessageStatus(state, action);
    default:
      return state;
  }
};

export default reducer;
