import { useEffect, useState } from "react";
import { getFormSettings } from "../api/formSettingsApi";

export function useFormSettings() {
    const [settings, setSettings] = useState({
        pretest_enabled: false,
        pretest_url: null,
        posttest_enabled: false,
        posttest_url: null,
    });

    useEffect(() => {
        getFormSettings()
            .then(setSettings)
            .catch(err =>
                console.error("Error loading form settings", err)
            );
    }, []);

    return settings;
}
