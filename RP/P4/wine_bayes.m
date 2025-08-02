%% 1. Cargar y preprocesar datos
clear; close all; clc;

% Cargar conjunto de datos Wine (13 características, 3 clases)
% load wine.data
%load('wineData.mat');
wine = readtable('./data/Wine.csv');

X = wine{:, 1:13};    % Características
y = wine{:, 14};   

% Escalado Z-score
X_scaled = zscore(X);

% Reducción dimensional (PCA)
[coeff, score] = pca(X_scaled);
X_pca = score(:,1:3);

% División entrenamiento/prueba
rng(42);
cv = cvpartition(y, 'HoldOut', 0.3);
X_train = X_pca(cv.training,:);
y_train = y(cv.training);
X_test = X_pca(cv.test,:);
y_test = y(cv.test);

%% 2. Entrenar modelo Naive Bayes con Kernel
model = fitcnb(X_train(:,1:2), y_train,...
    'DistributionNames','kernel',...  % Usar estimación por kernel
    'Kernel','normal',...             % Kernel gaussiano
    'Support','unbounded');

%% 3. Evaluación
y_pred = predict(model, X_test(:,1:2));
precision = sum(y_pred == y_test)/numel(y_test);
fprintf('Precisión: %.2f\n', precision);

%% 4. Visualización 2D
figure
d = 0.1;
[x1Grid,x2Grid] = meshgrid(min(X_pca(:,1)):d:max(X_pca(:,1)),...
                     min(X_pca(:,2)):d:max(X_pca(:,2)));
xGrid = [x1Grid(:), x2Grid(:)];
[~,scorePred] = predict(model, xGrid);

gscatter(xGrid(:,1), xGrid(:,2), scorePred,...
    [0.8 0.8 0.8; 0.95 0.95 0.95; 0.9 0.9 0.9]);
hold on
h_train = gscatter(X_train(:,1), X_train(:,2), y_train, 'rgb','o',15);
h_test = gscatter(X_test(:,1), X_test(:,2), y_test, 'rgb','^',20, 'filled');
title('Clasificación Naive Bayes (Kernel)')
xlabel('PC1')
ylabel('PC2')
legend([h_train(1), h_test(1)], {'Entrenamiento','Prueba'})

%% 5. Visualización 3D
figure
scatter3(X_train(:,1), X_train(:,2), X_train(:,3), 40, y_train, 'filled')
hold on
scatter3(X_test(:,1), X_test(:,2), X_test(:,3), 100, y_test, '^', 'LineWidth',2)
xlabel('PC1')
ylabel('PC2')
zlabel('PC3')
title('Distribución 3D con Naive Bayes')
colormap jet
colorbar

%% 6. Comparación de distribuciones (Hiperparámetro)
distributions = {'normal', 'kernel'};
accuracies = zeros(1, length(distributions));

for i = 1:length(distributions)
    model_tuned = fitcnb(X_train(:,1:2), y_train,...
        'DistributionNames', distributions{i});
    y_pred = predict(model_tuned, X_test(:,1:2));
    accuracies(i) = sum(y_pred == y_test)/numel(y_test);
end

figure
bar(accuracies)
set(gca,'XTickLabel', distributions)
xlabel('Tipo de Distribución')
ylabel('Precisión')
title('Comparación de Distribuciones en Naive Bayes')