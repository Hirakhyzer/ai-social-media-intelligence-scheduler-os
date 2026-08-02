% Plot PostPilot OS metrics from generated CSV files.
resultsDir = fullfile('outputs','results');
figDir = fullfile('outputs','figures');
if ~exist(figDir, 'dir'); mkdir(figDir); end
calendarPath = fullfile(resultsDir, 'synthetic_content_calendar.csv');
analyticsPath = fullfile(resultsDir, 'synthetic_performance_analytics.csv');
if exist(calendarPath, 'file')
    calendar = readtable(calendarPath);
    figure; categoricalPlatforms = categorical(calendar.platform);
    histogram(categoricalPlatforms);
    title('Scheduled items by platform'); ylabel('Count');
    saveas(gcf, fullfile(figDir, 'matlab_calendar_platforms.png'));
end
if exist(analyticsPath, 'file')
    analytics = readtable(analyticsPath);
    figure; bar(categorical(analytics.platform), analytics.simulated_engagement_rate);
    title('Synthetic engagement rate by queued post'); ylabel('Engagement rate'); xtickangle(45);
    saveas(gcf, fullfile(figDir, 'matlab_engagement_rates.png'));
end
