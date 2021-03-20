import json5 from 'json5';
import { eventSource } from 'model/jobsApi';
import { getSpiders } from 'model/spidersApi';
import React, { useEffect, useState } from 'react';
import { useSnackbar } from 'notistack'

const initGlobalContext = () => {
  return { jobs: {}, spiders: [] }
}

export const GlobalContext = React.createContext({});

export const GlobalContextProvider = (props) => {
  const [context, setContext] = useState(initGlobalContext())
  const { enqueueSnackbar } = useSnackbar();

  eventSource.onmessage = function (e) {
    const tmpJobs = json5.parse(e.data)
    setContext({ ...context, jobs: tmpJobs })
  }

  eventSource.onerror = function (e) {
    console.error(e)
    enqueueSnackbar("Could not connect to the server", {
      variant: 'error',
      autoHideDuration: 3000,
    });
  }

  useEffect(() => {
    getSpiders()
      .then(spiders => setContext({ ...context, spiders: spiders }))
      .catch(e => enqueueSnackbar(e.toString(), {
        variant: 'error',
        autoHideDuration: 3000,
      }))
  }, [])



  return <GlobalContext.Provider value={context}>
    {props.children}
  </GlobalContext.Provider>
}