%% 1. Cargar y preprocesar datos
wine = readtable('Wine.csv');

X = wine{:, 1:13};    % Características
y = wine{:, 14};   

% Reducción dimensional (PCA)
[coeff, score] = pca(X);
X_pca = score(:,1:2); % Usar 2 componentes

% División entrenamiento/prueba
rng(42);
cv = cvpartition(y, 'HoldOut', 0.3);
X_train = X_pca(cv.training,:);
y_train = y(cv.training);
X_test = X_pca(cv.test,:);
y_test = y(cv.test);

%% 2. Entrenar árbol
arbol = fitctree(X_train, y_train,...
    'MaxDepth', 4,...
    'MinParentSize', 10,...
    'SplitCriterion', 'gdi'); % Gini

%% 3. Evaluación
y_pred = predict(arbol, X_test);
precision = sum(y_pred == y_test)/numel(y_test);
fprintf('Precisión: %.2f\n', precision);

%% 4. Visualizar estructura del árbol
view(arbol, 'Mode', 'graph');

%% 5. Fronteras de decisión en 2D
d = 0.1;
[x1Grid, x2Grid] = meshgrid(min(X_pca(:,1)):d:max(X_pca(:,1)),...
                     min(X_pca(:,2)):d:max(X_pca(:,2)));
xGrid = [x1Grid(:), x2Grid(:)];
[~,scorePred] = predict(arbol, xGrid);

figure
gscatter(xGrid(:,1), xGrid(:,2), scorePred,...
    [0.8 0.8 0.8; 0.95 0.95 0.95; 0.9 0.9 0.9]);
hold on
h_train = gscatter(X_train(:,1), X_train(:,2), y_train, 'rgb','o',15);
h_test = gscatter(X_test(:,1), X_test(:,2), y_test, 'rgb','^',20, 'filled');
title('Fronteras de Decisión - Árbol de Decisión')
xlabel('PC1')
ylabel('PC2')
legend([h_train(1), h_test(1)], {'Entrenamiento','Prueba'})

%% 6. Comparación de hiperparámetros (SplitCriterion)
criterios = {'gdi', 'deviance'};
precisiones = zeros(1, length(criterios));

for i = 1:length(criterios)
    arbol_tmp = fitctree(X_train, y_train,...
        'SplitCriterion', criterios{i},...
        'MaxDepth', 4);
    y_pred_tmp = predict(arbol_tmp, X_test);
    precisiones(i) = sum(y_pred_tmp == y_test)/numel(y_test);
end

figure
bar(precisiones)
set(gca, 'XTickLabel', criterios)
xlabel('Criterio de División')
ylabel('Precisión')
title('Comparación de Criterios de División')