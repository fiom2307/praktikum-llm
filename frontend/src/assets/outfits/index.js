const importAll = (requireContext) =>
    requireContext.keys().reduce((images, path) => {
        const key = path.replace("./", "").replace(/\.\w+$/, ""); // filename without extension
        images[key] = requireContext(path);
        return images;
    }, {});

// Automatically import ALL images in this folder
const images = importAll(require.context("./", false, /\.(png|jpe?g|svg)$/));

export default images;