%% 1. Cargar y preprocesar datos
%load wine.data
%X = wine(:,2:end);
%y = wine(:,1);

%% Carga y preprocesamiento de datos
clear; close all; clc;

% Cargar conjunto de datos Wine (13 características, 3 clases)
% load wine.data
%load('wineData.mat');
wine = readtable('Wine.csv');

X = wine{:, 1:13};    % Características
y = wine{:, 14};   

% Escalado Z-score
X_scaled = zscore(X);

% Reducción dimensional (PCA)
[coeff, score] = pca(X_scaled);
X_pca = score(:,1:3);  % Primeras 3 componentes

% División entrenamiento/prueba
rng(42);  % Semilla
cv = cvpartition(y, 'HoldOut', 0.3);
X_train = X_pca(cv.training,:);
y_train = y(cv.training);
X_test = X_pca(cv.test,:);
y_test = y(cv.test);

%% 2. Búsqueda de hiperparámetros
k_values = [3 5 7 9];
distance_metrics = {'euclidean', 'cityblock'};
results = zeros(length(k_values), length(distance_metrics));

for i = 1:length(k_values)
    for j = 1:length(distance_metrics)
        knn = fitcknn(X_train(:,1:2), y_train,...
            'NumNeighbors', k_values(i),...
            'Distance', distance_metrics{j});
        y_pred = predict(knn, X_test(:,1:2));
        results(i,j) = sum(y_pred == y_test)/numel(y_test);
    end
end

% Gráfico de resultados
figure
bar(results)
set(gca,'XTickLabel',k_values)
xlabel('Valores de k')
ylabel('Precisión')
legend({'Euclidiana','Manhattan'}, 'Location', 'best')
title('Comparación de Hiperparámetros')

%% 3. Mejor modelo (k=5, distancia Euclidiana)
best_knn = fitcknn(X_train(:,1:2), y_train,...
    'NumNeighbors',5, 'Distance','euclidean');

%% 4. Visualización 2D
figure
h(1:3) = gscatter(X_train(:,1), X_train(:,2), y_train, 'rgb','o',[],'on');
hold on
h(4:6) = gscatter(X_test(:,1), X_test(:,2), y_test, 'rgb','^',[],'on');
title('Distribución 2D de Clases')
xlabel('PC1')
ylabel('PC2')
legend([h(1),h(4)], {'Entrenamiento','Prueba'}, 'Location','best')

% Fronteras de decisión
d = 0.1;
[x1Grid,x2Grid] = meshgrid(min(X_pca(:,1)):d:max(X_pca(:,1)),...
                     min(X_pca(:,2)):d:max(X_pca(:,2)));
xGrid = [x1Grid(:),x2Grid(:)];
[~,scorePred] = predict(best_knn,xGrid);

figure
gscatter(xGrid(:,1),xGrid(:,2),scorePred,...
    [0.8 0.8 0.8; 0.95 0.95 0.95; 0.9 0.9 0.9]);
hold on
h = gscatter(X_train(:,1), X_train(:,2), y_train,'rgb','.',20);
title('Fronteras de Decisión KNN')
xlabel('PC1')
ylabel('PC2')

%% 5. Visualización 3D
figure
scatter3(X_train(:,1), X_train(:,2), X_train(:,3), 40, y_train, 'filled')
hold on
scatter3(X_test(:,1), X_test(:,2), X_test(:,3), 100, y_test, '^', 'LineWidth',2)
xlabel('PC1')
ylabel('PC2')
zlabel('PC3')
title('Visualización 3D con PCA')
colormap jet
colorbar