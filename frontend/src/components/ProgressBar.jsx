function ProgressBar({ label, earned, required }) {
  const value =
    required > 0
      ? Math.min(100, Math.round((earned / required) * 100))
      : 0;

  return (
    <div
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin="0"
      aria-valuemax="100"
      className="w-full mt-4"
    >

      <p className="text-sm font-bold text-white text-center">
        {label} {earned} / {required} ({value}%)
      </p>

      <div className="mt-2 h-2 w-full rounded-full bg-gray-200">
        <div
          className="h-full rounded-full bg-blue-600 transition-all"
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

export default ProgressBar;
