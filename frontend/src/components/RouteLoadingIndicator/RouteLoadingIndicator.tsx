import { useIsFetching } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useLocation, useNavigation } from "react-router-dom";
import FullPageSpinner from "../FullPageSpinner/FullPageSpinner";

const HIDE_DELAY_MS = 200;

export default function RouteLoadingIndicator() {
  const navigation = useNavigation();
  const location = useLocation();
  const isFetching = useIsFetching();
  const [visible, setVisible] = useState(false);

  const isRouteTransition =
    navigation.state === "loading" || navigation.state === "submitting";
  const isNetworkFetching = isFetching > 0;

  const shouldShow = isRouteTransition || isNetworkFetching;
  const label = navigation.state === "submitting" ? "Submitting" : "Loading";

  useEffect(() => {
    if (shouldShow) {
      setVisible(true);
      return;
    }
    const timeout = window.setTimeout(() => setVisible(false), HIDE_DELAY_MS);
    return () => window.clearTimeout(timeout);
  }, [shouldShow]);

  /**
   * If the path changes we ensure at least one frame shows the spinner,
   * even if the fetch resolves immediately, so users see feedback.
   */
  useEffect(() => {
    setVisible(true);
    const timeout = window.setTimeout(() => {
      if (!shouldShow) {
        setVisible(false);
      }
    }, HIDE_DELAY_MS);
    return () => window.clearTimeout(timeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname]);

  if (!visible) {
    return null;
  }

  return <FullPageSpinner label={label} />;
}
